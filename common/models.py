from django.db import models


# UD3.3.i: Almacena los días utilizados por los horarios semanales.
class DiaSemana(models.Model):
    codigo = models.PositiveSmallIntegerField(
        verbose_name='código',
        primary_key=True,
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
