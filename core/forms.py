from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row

from .models import (
    CategoriaServicio,
    ExcepcionHorario,
    HorarioSemanal,
    Peluquero,
    Reserva,
    Servicio,
)


# UD4.3.d: Reutiliza todos los campos de categoría en crear y actualizar.
class CategoriaServicioForm(forms.ModelForm):
    class Meta:
        model = CategoriaServicio
        fields = '__all__'

    # UD4.4.c: Muestra nombre y descripción en una única fila sencilla.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-4'),
                Column('descripcion', css_class='col-md-8'),
            ),
        )


# UD4.3.e: Define el formulario de servicios y valida su precio.
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'

    # UD4.4.c: Agrupa identificación, descripción y datos comerciales.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('categoria', css_class='col-md-4'),
                Column('nombre', css_class='col-md-8'),
            ),
            Row(
                Column('descripcion', css_class='col-md-12'),
            ),
            Row(
                Column('duracion_minutos', css_class='col-md-4'),
                Column('precio', css_class='col-md-4'),
                Column('activo', css_class='col-md-4'),
            ),
        )

    # UD4.3.e: Un servicio ofrecido no puede tener precio nulo o negativo.
    def clean_precio(self):
        precio = self.cleaned_data['precio']

        if precio <= 0:
            raise ValidationError(
                'El precio del servicio debe ser mayor que cero.'
            )

        return precio


# UD4.3.f: Reutiliza todos los campos de peluquero en ambas acciones.
class PeluqueroForm(forms.ModelForm):
    class Meta:
        model = Peluquero
        fields = '__all__'

    # UD4.4.c: Separa identidad, contacto y servicios del peluquero.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-6'),
                Column('apellidos', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('telefono', css_class='col-md-6'),
            ),
            Row(
                Column('servicios', css_class='col-md-9'),
                Column('activo', css_class='col-md-3'),
            ),
        )


# UD4.3.g: Define el horario semanal y valida la coherencia de sus horas.
class HorarioSemanalForm(forms.ModelForm):
    class Meta:
        model = HorarioSemanal
        fields = '__all__'

    # UD4.4.c: Organiza profesional, día, intervalo y estado del horario.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('peluquero', css_class='col-md-6'),
                Column('dia_semana', css_class='col-md-6'),
            ),
            Row(
                Column('hora_inicio', css_class='col-md-5'),
                Column('hora_fin', css_class='col-md-5'),
                Column('activo', css_class='col-md-2'),
            ),
        )

    # UD4.3.g: La hora final siempre debe ser posterior a la inicial.
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise ValidationError(
                'La hora de fin debe ser posterior a la hora de inicio.'
            )

        return cleaned_data


# UD4.3.h: Define las excepciones y evita fechas que ya han pasado.
class ExcepcionHorarioForm(forms.ModelForm):
    class Meta:
        model = ExcepcionHorario
        fields = '__all__'

    # UD4.4.c: Separa fecha, horas y motivo de la excepción.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('peluquero', css_class='col-md-6'),
                Column('fecha', css_class='col-md-6'),
            ),
            Row(
                Column('hora_inicio', css_class='col-md-5'),
                Column('hora_fin', css_class='col-md-5'),
                Column('cerrado', css_class='col-md-2'),
            ),
            Row(
                Column('motivo', css_class='col-md-12'),
            ),
        )

    # UD4.3.h: Una excepción solo puede afectar al presente o al futuro.
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']

        if fecha < timezone.localdate():
            raise ValidationError(
                'No se pueden crear excepciones en fechas pasadas.'
            )

        return fecha


# UD4.3.i: Recoge solo los datos elegidos manualmente para una reserva.
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        # ReservaMixin calcula fecha_fin, duración y precio; fecha_creacion
        # también la completa Django, por lo que no deben editarse a mano.
        fields = [
            'cliente',
            'peluquero',
            'servicios',
            'fecha_inicio',
            'estado',
        ]

    # UD4.4.c: Organiza los datos elegibles sin mostrar cálculos derivados.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='col-md-6'),
                Column('peluquero', css_class='col-md-6'),
            ),
            Row(
                Column('servicios', css_class='col-md-12'),
            ),
            Row(
                Column('fecha_inicio', css_class='col-md-6'),
                Column('estado', css_class='col-md-6'),
            ),
        )
