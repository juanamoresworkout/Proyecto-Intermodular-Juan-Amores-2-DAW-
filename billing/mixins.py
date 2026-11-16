# messages muestra el rechazo de la operación mediante un aviso rojo.
from django.contrib import messages

# UD4.2.g: Evita que los cobros superen el total de su factura.
class CobroMixin:
    def form_valid(self, form):
        # form.instance contiene el cobro validado, todavía pendiente de guardar.
        factura = form.instance.factura
        # Excluye el propio cobro al actualizar para no sumarlo dos veces.
        # Al crear, su pk es None y se conservan todos los cobros existentes.
        cobros_anteriores = factura.cobros.exclude(
            pk=form.instance.pk,
        )
        # Suma solamente los importes que ya pertenecen a esa factura.
        total_cobrado = sum(
            cobro.importe for cobro in cobros_anteriores
        )

        # Rechaza el formulario si el acumulado superaría el total facturado.
        if total_cobrado + form.instance.importe > factura.total:
            messages.error(
                self.request,
                'La suma de los cobros no puede superar '
                'el total de la factura.',
            )
            # Vuelve a mostrar los datos introducidos sin guardar el cobro.
            return self.form_invalid(form)

        # Si cumple la regla, CreateView/UpdateView realiza el guardado normal.
        return super().form_valid(form)
