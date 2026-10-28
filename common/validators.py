from django.core.validators import RegexValidator


# Validador reutilizable: acepta teléfonos españoles de 9 cifras con +34 opcional.
telefono_espanol = RegexValidator(
    regex=r'^(?:\+34)?[6789]\d{8}$',
    message=(
        'Introduce un teléfono español válido, '
        'por ejemplo 612345678 o +34612345678.'
    ),
)