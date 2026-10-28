from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction

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
    horario_compatible = HorarioSemanal.objects.filter(
        peluquero=peluquero,
        dia_semana=fecha.weekday(),
        activo=True,
        hora_inicio__lte=hora_inicio,
        hora_fin__gte=hora_fin,
    ).exists()

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

@transaction.atomic
def crear_reserva(cliente, peluquero, fecha_inicio, servicios):
    servicios = list(servicios)

        # El cliente debe estar activo.
    if not cliente or not cliente.activo:
        raise ValidationError('El cliente no está activo.')

    # El peluquero debe realizar todos los servicios elegidos.
    if any(
        not peluquero.servicios.filter(pk=servicio.pk).exists()
        for servicio in servicios
    ):
        raise ValidationError(
            'El peluquero no realiza todos los servicios seleccionados.'
        )

    # Calcula los totales y valida los servicios.
    fecha_fin, duracion, precio = calcular_datos_reserva(
        fecha_inicio, servicios,
    )

    # Comprueba que la cita sea futura, quepa en el horario y no coincida con otra reserva.
    if not esta_disponible(peluquero, fecha_inicio, fecha_fin):
        raise ValidationError('El horario no está disponible.')

    reserva = Reserva.objects.create(
        cliente=cliente,
        peluquero=peluquero,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        duracion_total_minutos=duracion,
        precio_total=precio,
    )
    reserva.servicios.set(servicios)

    return reserva