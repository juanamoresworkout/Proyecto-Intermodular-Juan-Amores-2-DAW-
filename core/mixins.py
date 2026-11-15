# messages publica los errores de reserva en la plantilla común.
from django.contrib import messages
# ValidationError permite capturar las reglas incumplidas por el servicio.
from django.core.exceptions import ValidationError

# La lógica de negocio se centraliza en services y no se duplica en la vista.
from .services import validar_reserva


# UD4.2.h: Valida y calcula los datos comunes al crear o actualizar reservas.
class ReservaMixin:
    def form_valid(self, form):
        # cleaned_data contiene los valores ya comprobados por el formulario.
        cliente = form.cleaned_data['cliente']
        peluquero = form.cleaned_data['peluquero']
        # Convierte la selección múltiple para poder recorrerla varias veces.
        servicios = list(form.cleaned_data['servicios'])
        fecha_inicio = form.cleaned_data['fecha_inicio']

        # UD4.2.h: Al actualizar, no compara la reserva consigo misma.
        reserva_actual = (
            self.object
            if self.object and self.object.pk
            else None
        )

        try:
            # El servicio valida la reserva y devuelve sus campos calculados.
            fecha_fin, duracion, precio = validar_reserva(
                cliente,
                peluquero,
                fecha_inicio,
                servicios,
                reserva_actual=reserva_actual,
            )
        except ValidationError as error:
            # Utiliza el primer mensaje concreto para explicar el rechazo.
            return self._formulario_invalido(
                form,
                error.messages[0],
            )

        # UD4.2.h: Estos campos no se muestran porque son cálculos derivados
        # de la fecha inicial y de los servicios seleccionados.
        form.instance.fecha_fin = fecha_fin
        form.instance.duracion_total_minutos = duracion
        form.instance.precio_total = precio

        # La vista padre guarda la reserva y su relación de servicios.
        return super().form_valid(form)

    def _formulario_invalido(self, form, mensaje):
        # Publica el mismo motivo como aviso rojo y error general del formulario.
        messages.error(self.request, mensaje)
        form.add_error(None, mensaje)
        # Renderiza de nuevo el formulario sin guardar ningún cambio.
        return super().form_invalid(form)
