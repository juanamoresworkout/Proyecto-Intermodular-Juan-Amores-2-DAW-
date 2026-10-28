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

        constraints = [
            models.UniqueConstraint(
                fields=['categoria', 'nombre'],
                name='servicio_categoria_nombre_unico',
            ),
        ]

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
    dia_semana = models.PositiveSmallIntegerField(
        choices=DiaSemana.choices,
    )
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    # Compara el nuevo bloque con los horarios del mismo peluquero y día.
    def clean(self):
        super().clean()

        if (
            not self.activo
            or not self.peluquero_id
            or self.dia_semana is None
            or not self.hora_inicio
            or not self.hora_fin
            or self.hora_inicio >= self.hora_fin
        ):
            return

        horarios_existentes = HorarioSemanal.objects.filter(
            peluquero_id=self.peluquero_id,
            dia_semana=self.dia_semana,
            activo=True,
        ).exclude(pk=self.pk).values_list(
            'hora_inicio',
            'hora_fin',
        )

        for inicio_existente, fin_existente in horarios_existentes:
            empieza_antes_de_que_termine = self.hora_inicio < fin_existente
            termina_despues_de_que_empiece = self.hora_fin > inicio_existente

            if empieza_antes_de_que_termine and termina_despues_de_que_empiece:
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

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'peluquero',
                    'dia_semana',
                    'hora_inicio',
                    'hora_fin',
                ],
                name='horario_semanal_bloque_unico',
            ),
            models.CheckConstraint(
                condition=models.Q(
                    hora_fin__gt=models.F('hora_inicio'),
                ),
                name='horario_semanal_horas_validas',
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
    peluquero = models.ForeignKey(
        Peluquero,
        on_delete=models.CASCADE,
        related_name='excepciones_horario',
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField(
        null=True,
        blank=True,
    )
    hora_fin = models.TimeField(
        null=True,
        blank=True,
    )
    cerrado = models.BooleanField(default=False)
    motivo = models.CharField(
        max_length=255,
        blank=True,
    )

    # Comprueba que solo exista una excepción coherente por peluquero y fecha.
    def clean(self):
        super().clean()

        if not self.peluquero_id or not self.fecha:
            return

        if self.fecha < timezone.localdate():
            raise ValidationError({
                'fecha': 'No se pueden crear excepciones en fechas pasadas.',
            })

        excepcion_existente = ExcepcionHorario.objects.filter(
            peluquero_id=self.peluquero_id,
            fecha=self.fecha,
        ).exclude(pk=self.pk).exists()

        if excepcion_existente:
            raise ValidationError(
                'Ya existe una excepción para este peluquero y fecha. '
                'Debes modificarla o eliminarla antes.'
            )

        if self.cerrado:
            if self.hora_inicio or self.hora_fin:
                raise ValidationError(
                    'Un día cerrado no puede tener horas.'
                )

            return

        if not self.hora_inicio or not self.hora_fin:
            raise ValidationError(
                'Una excepción abierta necesita hora de inicio y de fin.'
            )

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

        constraints = [
            models.UniqueConstraint(
                fields=['peluquero', 'fecha'],
                name='excepcion_peluquero_fecha_unica',
            ),
        ]

    def __str__(self):
        if self.cerrado:
            return f'{self.peluquero} - cerrado el {self.fecha}'

        return (
            f'{self.peluquero} - {self.fecha} '
            f'de {self.hora_inicio} a {self.hora_fin}'
        )

# UD3.3.h: Representa una cita reservada por un cliente.
class Reserva(models.Model):
    class Estado(models.TextChoices):
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
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
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