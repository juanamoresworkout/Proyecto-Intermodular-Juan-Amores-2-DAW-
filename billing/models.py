from django.db import models
from django.utils import timezone

from common.validators import telefono_espanol

# UD3.3.g: Almacena los datos personales y de contacto del cliente.
class Cliente(models.Model):
    nombre = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=512)
    nif = models.CharField(
        max_length=20,
        unique=True,
    )
    email = models.EmailField(unique=True)
    telefono = models.CharField(
        max_length=12,
        validators=[telefono_espanol],
        blank=True,
    )
    activo = models.BooleanField(default=True)

    # UD3.4.e: Define los nombres del modelo en el administrador.
    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        # UD3.4.f: Ordena por apellidos y, en caso de empate, por nombre.
        ordering = ['apellidos', 'nombre']

    # UD3.3.b: Muestra nombre, apellidos y NIF según el anexo I.
    def __str__(self):
        return f'{self.nombre} {self.apellidos} ({self.nif})'

# Almacena una factura emitida a un cliente.
class Factura(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='facturas',
    )
    numero = models.CharField(
        max_length=20,
        unique=True,
    )
    concepto = models.TextField()
    fecha = models.DateField(default=timezone.now)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        # UD3.4.e: Nombres singular y plural del modelo.
        verbose_name = 'factura'
        verbose_name_plural = 'facturas'

        # UD3.4.f: Ordena por número de factura.
        ordering = ['numero']

    # UD3.3.b: Muestra el cliente y el número de factura.
    def __str__(self):
        return f'{self.cliente} - {self.numero}'

# Almacena un pago recibido para una factura.
class Cobro(models.Model):
    factura = models.ForeignKey(
        Factura,
        on_delete=models.PROTECT,
        related_name='cobros',
    )
    fecha = models.DateField(default=timezone.now)
    importe = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        # UD3.4.e: Nombres singular y plural del modelo.
        verbose_name = 'cobro'
        verbose_name_plural = 'cobros'

        # UD3.4.f: Muestra primero los cobros más recientes.
        ordering = ['-fecha']

    # UD3.3.b: Muestra el número de factura y el importe cobrado.
    def __str__(self):
        return f'{self.factura.numero} - {self.importe}'