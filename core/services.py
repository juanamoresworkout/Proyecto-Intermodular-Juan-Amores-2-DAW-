# Lógica preparada para crear reservas de forma segura.
# Falta conectarla a una vista o formulario: las vistas actuales solo
# muestran listas y detalles, por lo que crear_reserva todavía no se llama.

# timedelta permite sumar minutos a la fecha de inicio de una reserva.
from datetime import timedelta
# Decimal mantiene exactos los cálculos de precios.
from decimal import Decimal

# ValidationError comunica que una regla de negocio no se cumple.
from django.core.exceptions import ValidationError
# timezone usa la fecha, la hora y la zona horaria configuradas en Django.
from django.utils import timezone
# transaction permite que la creación completa se guarde o se deshaga junta.
from django.db import transaction

# Modelos que se consultan o se crean desde este archivo.
from .models import ExcepcionHorario, HorarioSemanal, Reserva


# Comprueba que la reserva empiece en el futuro y termine después de empezar.
def intervalo_es_valido(fecha_inicio, fecha_fin) -> bool:
    # Solo devuelve True cuando se cumple: ahora < inicio < fin.
    return timezone.now() < fecha_inicio < fecha_fin


# Comprueba si la cita cabe en la excepción o en el horario semanal.
def cabe_en_horario(peluquero, fecha_inicio, fecha_fin) -> bool:
    # Un peluquero inactivo no puede recibir nuevas reservas.
    if not peluquero.activo:
        return False

    # Convierte las fechas y horas a la zona horaria local del proyecto.
    inicio_local = timezone.localtime(fecha_inicio)
    fin_local = timezone.localtime(fecha_fin)

    # No permitimos que una misma cita empiece y termine en días diferentes.
    if inicio_local.date() != fin_local.date():
        return False

    # Separa la fecha y las horas para poder compararlas con los horarios.
    fecha = inicio_local.date()
    hora_inicio = inicio_local.time()
    hora_fin = fin_local.time()

    # Busca si el peluquero tiene un horario especial para esta fecha.
    excepcion = ExcepcionHorario.objects.filter(
        peluquero=peluquero,
        fecha=fecha,
    ).first()

    # Si existe una excepción, sustituye completamente al horario semanal.
    if excepcion:
        # Si la excepción marca el día como cerrado, no se puede reservar.
        if excepcion.cerrado:
            return False

        # La cita solo cabe si empieza y termina dentro de la excepción.
        return (
            hora_inicio >= excepcion.hora_inicio
            and hora_fin <= excepcion.hora_fin
        )

    # Si no hay excepción, busca un bloque semanal que contenga toda la cita.
    horario_compatible = (
        HorarioSemanal.objects.filter(
            # Debe pertenecer al peluquero elegido para la reserva.
            peluquero=peluquero,
            # weekday convierte la fecha en un día de 0 a 6.
            dia_semana=fecha.weekday(),
            # Los horarios desactivados no permiten recibir reservas.
            activo=True,
            # El bloque debe empezar antes o a la vez que la cita.
            hora_inicio__lte=hora_inicio,
            # El bloque debe terminar después o a la vez que la cita.
            hora_fin__gte=hora_fin,
        )
        # Devuelve True si encuentra un bloque completo y False si no.
        .exists()
    )

    # Devuelve True si encontró al menos un bloque compatible; si no, False.
    return horario_compatible


# Comprueba que el peluquero no tenga otra reserva durante ese intervalo.
def peluquero_esta_libre(peluquero, fecha_inicio, fecha_fin) -> bool:
    # Busca reservas del mismo peluquero que se crucen con la nueva cita.
    reserva_solapada = Reserva.objects.filter(
        peluquero=peluquero,
        fecha_inicio__lt=fecha_fin,
        fecha_fin__gt=fecha_inicio,
    ).exclude(
        # Las reservas canceladas ya no ocupan tiempo.
        estado=Reserva.Estado.CANCELADA,
    ).exists()

    # Si encuentra una reserva solapada, devuelve False; si no, True.
    return not reserva_solapada


# Devuelve True solamente si la cita cumple todas las condiciones.
def esta_disponible(peluquero, fecha_inicio, fecha_fin) -> bool:
    # and detiene la comprobación en cuanto una condición devuelve False.
    return (
        intervalo_es_valido(fecha_inicio, fecha_fin)
        and cabe_en_horario(peluquero, fecha_inicio, fecha_fin)
        and peluquero_esta_libre(peluquero, fecha_inicio, fecha_fin)
    )


# Calcula la duración, el precio y la hora final a partir de los servicios.
def calcular_datos_reserva(fecha_inicio, servicios):
    # Convierte los servicios en una lista para poder recorrerlos varias veces.
    lista_servicios = list(servicios)

    # Una reserva siempre debe contener, como mínimo, un servicio.
    if not lista_servicios:
        raise ValidationError(
            'La reserva debe incluir al menos un servicio.'
        )

    # any() devuelve True si encuentra al menos un servicio inactivo.
    if any(not servicio.activo for servicio in lista_servicios):
        raise ValidationError(
            'No se puede reservar un servicio inactivo.'
        )

    # Suma los minutos de todos los servicios seleccionados.
    duracion_total = sum(
        servicio.duracion_minutos
        for servicio in lista_servicios
    )

    # Suma los precios con Decimal para mantener exactos los importes monetarios.
    precio_total = sum(
        (servicio.precio for servicio in lista_servicios),
        Decimal('0.00'),
    )

    # Calcula el final añadiendo la duración total a la fecha y hora de inicio.
    fecha_fin = fecha_inicio + timedelta(
        minutes=duracion_total,
    )

    # Devuelve los tres datos para utilizarlos al crear la reserva.
    return fecha_fin, duracion_total, precio_total

# Ejecuta toda la función dentro de una transacción. Si ocurre un error,
# evita guardar una reserva a medias.
@transaction.atomic
def crear_reserva(cliente, peluquero, fecha_inicio, servicios):
    # Convierte los servicios en una lista para poder recorrerlos varias veces.
    servicios = list(servicios)

    # No permite reservar sin cliente ni con un cliente inactivo.
    if not cliente or not cliente.activo:
        raise ValidationError('El cliente no está activo.')

    # Recorre los servicios y comprueba que el peluquero tenga asignado cada uno.
    if any(
        # Si no encuentra el servicio entre los del peluquero, devuelve True.
        not peluquero.servicios.filter(pk=servicio.pk).exists()
        for servicio in servicios
    ):
        raise ValidationError(
            'El peluquero no realiza todos los servicios seleccionados.'
        )

    # Valida los servicios y recibe la hora final, la duración y el precio.
    fecha_fin, duracion, precio = calcular_datos_reserva(
        fecha_inicio, servicios,
    )

    # Comprueba que la cita sea futura, quepa en el horario y no se solape.
    if not esta_disponible(peluquero, fecha_inicio, fecha_fin):
        raise ValidationError('El horario no está disponible.')

    # Crea primero la reserva con los campos que no son muchos a muchos.
    reserva = Reserva.objects.create(
        cliente=cliente,
        peluquero=peluquero,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        duracion_total_minutos=duracion,
        precio_total=precio,
    )
    # Guarda después los servicios en la tabla intermedia de la relación M2M.
    reserva.servicios.set(servicios)

    # Devuelve el objeto creado para que la futura vista pueda utilizarlo.
    return reserva
