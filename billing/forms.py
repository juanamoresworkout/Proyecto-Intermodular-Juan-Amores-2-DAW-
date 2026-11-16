from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row

from .models import Cliente, Cobro, Factura


# UD4.3.a: Define el formulario reutilizado para crear y actualizar clientes.
class ClienteForm(forms.ModelForm):
    # Meta relaciona este formulario con su modelo y selecciona sus campos.
    class Meta:
        model = Cliente
        # Incluye todos los campos editables definidos actualmente en Cliente.
        fields = '__all__'

    # UD4.4.c: Configura la presentación Bootstrap 5 del formulario de cliente.
    def __init__(self, *args, **kwargs):
        # ModelForm debe crear sus campos antes de organizar el layout.
        super().__init__(*args, **kwargs)

        # FormHelper comunica a Crispy la configuración de presentación.
        self.helper = FormHelper()
        # La plantilla común ya contiene el elemento form y sus botones.
        self.helper.form_tag = False
        # Bootstrap divide cada fila en doce columnas.
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-3'),
                Column('apellidos', css_class='col-md-6'),
                Column('nif', css_class='col-md-3'),
            ),
            Row(
                Column('email', css_class='col-md-12'),
            ),
            Row(
                Column('telefono', css_class='col-md-6'),
                Column('activo', css_class='col-md-6'),
            ),
        )


# UD4.3.b: Define y valida el formulario de alta y modificación de facturas.
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        # La factura expone todos sus campos editables en ambas vistas.
        fields = '__all__'

    # UD4.4.c: Distribuye la factura según el grid indicado en el anexo.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='col-md-12'),
            ),
            Row(
                Column('numero', css_class='col-md-4'),
                Column('fecha', css_class='col-md-4'),
                Column('total', css_class='col-md-4'),
            ),
            Row(
                Column('concepto', css_class='col-md-12'),
            ),
        )

    # UD4.3.b: Impide guardar un total igual o inferior a cero.
    def clean_total(self):
        # cleaned_data ya contiene el valor convertido a Decimal por Django.
        total = self.cleaned_data['total']

        if total <= 0:
            raise ValidationError(
                'El total de la factura debe ser mayor que cero.'
            )

        # Devuelve el valor validado para que el formulario pueda guardarlo.
        return total


# UD4.3.c: Define y valida el formulario de alta y modificación de cobros.
class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        # Ambas vistas reciben todos los campos editables del cobro.
        fields = '__all__'

    # UD4.4.c: Coloca la factura sola y reparte fecha e importe por igual.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('factura', css_class='col-md-12'),
            ),
            Row(
                Column('fecha', css_class='col-md-6'),
                Column('importe', css_class='col-md-6'),
            ),
        )

    # UD4.3.c: Impide guardar un importe igual o inferior a cero.
    def clean_importe(self):
        # Django convierte previamente el texto introducido en Decimal.
        importe = self.cleaned_data['importe']

        if importe <= 0:
            raise ValidationError(
                'El importe del cobro debe ser mayor que cero.'
            )

        # Conserva el importe limpio para el resto de validaciones y guardado.
        return importe
