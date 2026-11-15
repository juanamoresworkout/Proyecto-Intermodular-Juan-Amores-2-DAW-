# Los validadores rechazan códigos fuera del intervalo antes de guardarlos.
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# UD3.3.i: Almacena los días utilizados por los horarios semanales.
class DiaSemana(models.Model):
    codigo = models.PositiveSmallIntegerField(
        verbose_name='código',
        primary_key=True,
        # Python y los formularios solo aceptan los siete valores de weekday().
        validators=[
            MinValueValidator(0),
            MaxValueValidator(6),
        ],
    )
    nombre = models.CharField(
        verbose_name='nombre',
        max_length=20,
        unique=True,
    )

    class Meta:
        verbose_name = 'día de la semana'
        verbose_name_plural = 'días de la semana'
        ordering = ['codigo']
        # La restricción repite la protección directamente en la base de datos.
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    codigo__gte=0,
                    codigo__lte=6,
                ),
                name='dia_semana_codigo_entre_0_y_6',
                # full_clean puede utilizar este texto al incumplir la regla.
                violation_error_message=(
                    'El código del día debe estar comprendido entre 0 y 6.'
                ),
            ),
        ]

    def __str__(self):
        return self.nombre


# UD3.3.j: Almacena los estados permitidos para las reservas.
class EstadoReserva(models.Model):
    codigo = models.CharField(
        verbose_name='código',
        max_length=20,
        primary_key=True,
    )
    nombre = models.CharField(
        verbose_name='nombre',
        max_length=30,
        unique=True,
    )

    class Meta:
        verbose_name = 'estado de reserva'
        verbose_name_plural = 'estados de reserva'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
