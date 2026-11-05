from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone 

from common.validators import telefono_espanol


# UD3.3.a: Define las categorías que agrupan los servicios de la peluquería.
class CategoriaServicio(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
    )
    descripcion = models.CharField(
        max_length=255,
        blank=True,
    )

    class Meta:
        # UD3.4.e: Nombres del modelo.
        verbose_name = 'categoría de servicio'
        verbose_name_plural = 'categorías de servicios'

        # UD3.4.f: Orden alfabético por nombre.
        ordering = ['nombre']

    # UD3.3.b: Muestra la categoría mediante su nombre.
    def __str__(self):
        return self.nombre


# UD3.3.c: Representa cada servicio ofrecido por la peluquería.
class Servicio(models.Model):
    categoria = models.ForeignKey(
        CategoriaServicio,
        # Impide eliminar una categoría mientras tenga servicios asociados.
        on_delete=models.PROTECT,
        related_name='servicios',
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(
        max_length=255,
        blank=True,
    )
    duracion_minutos = models.PositiveIntegerField()
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    activo = models.BooleanField(default=True)

    # Impide repetir el nombre de un servicio dentro de la misma categoría.
    class Meta:
        # UD3.4.e: Nombres singular y plural del modelo.
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'

        # UD3.4.f: Ordena por nombre de categoría y después por servicio.
        ordering = ['categoria__nombre', 'nombre']

        # UD3.3.c: Impide repetir un servicio dentro de la misma categoría.
        unique_together = (
            ('categoria', 'nombre'),
        )

    def __str__(self):
        return self.nombre


# UD3.3.d: Representa a los peluqueros y los servicios que pueden realizar.
class Peluquero(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    # Si el teléfono no es español, el validador genera un error de validación.
    telefono = models.CharField(
        max_length=12,
        validators=[telefono_espanol],
        blank=True,
    )
    servicios = models.ManyToManyField(
        Servicio,
        related_name='peluqueros',
        blank=True,
    )
    # Permite ocultar al peluquero de nuevas reservas sin eliminar sus datos.
    activo = models.BooleanField(default=True)

    class Meta:
        # UD3.4.e: Nombres del modelo.
        verbose_name = 'peluquero'
        verbose_name_plural = 'peluqueros'

        # UD3.4.f: Ordena por apellidos y nombre.
        ordering = ['apellidos', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'


# UD3.3.e: Define el horario habitual de un peluquero para cada día semanal.
class HorarioSemanal(models.Model):
    class DiaSemana(models.IntegerChoices):
        LUNES = 0, 'Lunes'
        MARTES = 1, 'Martes'
        MIERCOLES = 2, 'Miércoles'
        JUEVES = 3, 'Jueves'
        VIERNES = 4, 'Viernes'
        SABADO = 5, 'Sábado'
        DOMINGO = 6, 'Domingo'

    peluquero = models.ForeignKey(
        Peluquero,
        on_delete=models.CASCADE,
        related_name='horarios_semanales',
    )
    #limita el campo a los días definidos y muestra sus etiquetas en formularios.
    dia_semana = models.PositiveSmallIntegerField(
        choices=DiaSemana.choices,
    )
    #Guarda horas sin fecha
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    # Compara el nuevo bloque con los horarios del mismo peluquero y día.
    def clean(self):
        # Mantiene las validaciones heredadas de models.Model.
        super().clean()

        # Sale sin comparar si faltan datos o el intervalo no es valido.
        if (
            not self.activo
            or not self.peluquero_id
            # El lunes vale 0, por eso se compara expresamente con None.
            or self.dia_semana is None
            or not self.hora_inicio
            or not self.hora_fin
            or self.hora_inicio >= self.hora_fin
        ):
            return

        # Busca bloques activos del mismo peluquero y del mismo día.
        horarios_existentes = (
            HorarioSemanal.objects.filter(
                peluquero_id=self.peluquero_id,
                dia_semana=self.dia_semana,
                activo=True,
            )
            # Al editar, evita compararlo con su propio registro.
            .exclude(pk=self.pk)
            # Solo recupera las horas, que son los datos necesarios.
            .values_list(
                'hora_inicio',
                'hora_fin',
            )
        )

        # Compara el nuevo intervalo con cada bloque que ya existe.
        for inicio_existente, fin_existente in horarios_existentes:
            # Empieza antes de que termine el bloque existente.
            empieza_antes_de_que_termine = self.hora_inicio < fin_existente
            # Termina despues de que empiece el bloque existente.
            termina_despues_de_que_empiece = self.hora_fin > inicio_existente

            if empieza_antes_de_que_termine and termina_despues_de_que_empiece:
                # Si se cumplen ambas condiciones, los horarios se solapan.
                raise ValidationError(
                    'Este horario se solapa con otro bloque semanal '
                    'del peluquero.'
                )

    # Evita bloques repetidos y exige que la hora final sea posterior a la inicial.
    class Meta:
        # UD3.4.e: Nombres del modelo.
        verbose_name = 'horario semanal'
        verbose_name_plural = 'horarios semanales'

        # UD3.4.f: Agrupa por peluquero, día y hora.
        ordering = ['peluquero', 'dia_semana', 'hora_inicio']

        # UD3.3.c: Impide repetir exactamente el mismo bloque semanal.
        unique_together = (
            ('peluquero', 'dia_semana', 'hora_inicio', 'hora_fin'),
        )

        # UD3.3.c: Exige que el bloque termine después de comenzar.
        constraints = [
            # Crea una regla que también se comprueba en la base de datos.
            models.CheckConstraint(
                # Define la condición que debe cumplir cada horario.
                condition=models.Q(
                    # __gt significa "mayor que" y F permite comparar
                    # hora_fin con hora_inicio dentro del mismo registro.
                    hora_fin__gt=models.F('hora_inicio'),
                ),
                # Nombre usado para identificar la regla en la migración
                # y en la base de datos.
                name='horario_semanal_horas_validas',
                # Mensaje que explica el error cuando no se cumple la regla.
                violation_error_message=(
                    'La hora de fin debe ser posterior a la hora de inicio.'
                ),
            ),
        ]
    def __str__(self):
        return (
            f'{self.peluquero} - {self.get_dia_semana_display()} '
            f'de {self.hora_inicio} a {self.hora_fin}'
        )

# UD3.3.f: Modifica el horario de un peluquero en una fecha concreta.
class ExcepcionHorario(models.Model):
    # Indica a que peluquero afecta la excepcion. Si se borra el
    # peluquero, tambien se borran sus excepciones.
    peluquero = models.ForeignKey(
        Peluquero,
        on_delete=models.CASCADE,
        related_name='excepciones_horario',
    )
    # Dia concreto en el que se cambia el horario habitual.
    fecha = models.DateField()
    # Las horas pueden quedar vacias cuando ese dia esta cerrado.
    hora_inicio = models.TimeField(
        null=True,
        blank=True,
    )
    hora_fin = models.TimeField(
        null=True,
        blank=True,
    )
    # Indica si el peluquero no trabaja durante toda esa fecha.
    cerrado = models.BooleanField(default=False)
    # Permite explicar el motivo del cierre o del horario especial.
    motivo = models.CharField(
        max_length=255,
        blank=True,
    )

    # Comprueba que solo exista una excepción coherente por peluquero y fecha.
    def clean(self):
        # Mantiene las validaciones heredadas de models.Model.
        super().clean()

        # Sin peluquero o fecha todavia no se puede comprobar la excepcion.
        if not self.peluquero_id or not self.fecha:
            return

        # No permite preparar cambios para dias que ya han pasado.
        if self.fecha < timezone.localdate():
            raise ValidationError({
                'fecha': 'No se pueden crear excepciones en fechas pasadas.',
            })

        # Busca otra excepcion del mismo peluquero y la misma fecha.
        excepcion_existente = (
            ExcepcionHorario.objects.filter(
                peluquero_id=self.peluquero_id,
                fecha=self.fecha,
            )
            # Al editar, evita compararla con su propio registro.
            .exclude(pk=self.pk)
            # Solo necesitamos saber si existe, no recuperar el objeto.
            .exists()
        )

        # Solo puede existir una excepcion por peluquero y fecha.
        if excepcion_existente:
            raise ValidationError(
                'Ya existe una excepción para este peluquero y fecha. '
                'Debes modificarla o eliminarla antes.'
            )

        # Un dia cerrado no necesita horas y tampoco debe tenerlas.
        if self.cerrado:
            if self.hora_inicio or self.hora_fin:
                raise ValidationError(
                    'Un día cerrado no puede tener horas.'
                )

            return

        # Si el dia esta abierto, necesita tanto la hora inicial como la final.
        if not self.hora_inicio or not self.hora_fin:
            raise ValidationError(
                'Una excepción abierta necesita hora de inicio y de fin.'
            )

        # Evita horarios iguales o intervalos que terminan antes de empezar.
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError(
                'La hora de fin debe ser posterior a la hora de inicio.'
            )

    # Solo permite una excepción por peluquero y fecha.
    class Meta:
        # UD3.4.e: Nombres del modelo.
        verbose_name = 'excepción de horario'
        verbose_name_plural = 'excepciones de horario'

        # UD3.4.f: Muestra primero las fechas más recientes.
        ordering = ['-fecha', 'peluquero']
        # UD3.3.c: Solo permite una excepción por peluquero y fecha.
        unique_together = (
            ('peluquero', 'fecha'),
        )

    def __str__(self):
        # Para un cierre solo muestra el peluquero y la fecha.
        if self.cerrado:
            return f'{self.peluquero} - cerrado el {self.fecha}'

        # Para un dia abierto muestra tambien su horario especial.
        return (
            f'{self.peluquero} - {self.fecha} '
            f'de {self.hora_inicio} a {self.hora_fin}'
        )

# UD3.3.h: Representa una cita reservada por un cliente.
class Reserva(models.Model):
    # Define los cuatro estados posibles de una reserva. Se usa TextChoices
    # porque un BooleanField solo permitiria dos opciones.
    class Estado(models.TextChoices):
        # El primer texto se guarda en la base de datos y el segundo es
        # la etiqueta que se muestra en formularios y en el administrador.
        PENDIENTE = 'pendiente', 'Pendiente'
        CONFIRMADA = 'confirmada', 'Confirmada'
        CANCELADA = 'cancelada', 'Cancelada'
        COMPLETADA = 'completada', 'Completada'

    cliente = models.ForeignKey(
        'billing.Cliente',
        on_delete=models.SET_NULL,
        related_name='reservas',
        null=True,
    )
    peluquero = models.ForeignKey(
        Peluquero,
        on_delete=models.PROTECT,
        related_name='reservas',
    )
    servicios = models.ManyToManyField(
        Servicio,
        related_name='reservas',
    )
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    duracion_total_minutos = models.PositiveIntegerField()
    precio_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    # Guarda el estado como texto, pero solo permite las opciones de Estado.
    estado = models.CharField(
        # La opcion mas larga cabe dentro del limite de 20 caracteres.
        max_length=20,
        # Convierte la enumeracion en las opciones del campoentr.
        choices=Estado.choices,
        # Una reserva nueva empieza pendiente si no se indica otro estado.
        default=Estado.PENDIENTE,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        # UD3.4.e: Nombres del modelo.
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'

        # UD3.4.f: Muestra primero las citas más lejanas en el tiempo.
        ordering = ['-fecha_inicio']

    def __str__(self):
        return (
            f'Reserva {self.pk} - {self.fecha_inicio} '
            f'- {self.peluquero}'
        )
