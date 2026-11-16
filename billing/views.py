from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy

from common.mixins import (
    CreateUpdateContextMixin,
    CreateUpdateSuccessMixin,
    DeleteContextMixin,
    OrderingMixin,
    ProtectedDeleteMixin,
)

# UD4.3: Los ModelForm centralizan campos y validaciones de ambas acciones.
from .forms import ClienteForm, CobroForm, FacturaForm
from .mixins import CobroMixin
from .models import Cliente, Factura, Cobro

# UD4.2: Los mixins se sitúan a la izquierda de la vista genérica para
# ejecutar primero la ordenación, la validación o la protección compartida.
# En Create/Update, fields limita los datos editables y los atributos de texto
# alimentan la plantilla común; en Delete, success_url vuelve a cada listado.

# UD3.7.a: Muestra el listado de clientes.
class ClienteListView(OrderingMixin, ListView):
    model = Cliente
    template_name = 'billing/cliente_list.html'
    paginate_by = 5


# UD3.7.a: Muestra los datos de un cliente concreto.
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'billing/cliente_detail.html'

# UD4.2.a: Permite crear clientes mediante el formulario generado por Django.
class ClienteCreateView(
    CreateUpdateSuccessMixin,
    CreateUpdateContextMixin,
    CreateView,
):
    model = Cliente
    # La vista delega la generación y validación en el ModelForm.
    form_class = ClienteForm
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear cliente'
    titulo_actualizacion = None
    url_borrado = None
    success_url_name = 'cliente_update'
    success_message = "Cliente '{object}' creado correctamente."


# UD4.2.a: Permite modificar los datos de un cliente existente.
class ClienteUpdateView(
    CreateUpdateSuccessMixin,
    CreateUpdateContextMixin,
    UpdateView,
):
    model = Cliente
    # Reutiliza el mismo formulario para mantener idénticas reglas y campos.
    form_class = ClienteForm
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar cliente'
    url_borrado = 'cliente_delete'
    success_url_name = 'cliente_update'
    success_message = "Cliente '{object}' actualizado correctamente."


# UD4.2.a: Solicita confirmación antes de eliminar un cliente.
class ClienteDeleteView(ProtectedDeleteMixin, DeleteContextMixin, DeleteView):
    model = Cliente
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar cliente'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar el cliente {object}?'
    )
    success_url = reverse_lazy('cliente_list')

# UD3.7.a: Muestra el listado completo de facturas.
class FacturaListView(OrderingMixin, ListView):
    model = Factura
    template_name = 'billing/factura_list.html'
    paginate_by = 5

# UD3.7.a: Muestra los datos de una factura concreta.
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'billing/factura_detail.html'


# UD4.2.a: Permite crear facturas mediante el formulario generado por Django.
class FacturaCreateView(
    CreateUpdateSuccessMixin,
    CreateUpdateContextMixin,
    CreateView,
):
    model = Factura
    # FacturaForm impide guardar totales iguales o inferiores a cero.
    form_class = FacturaForm
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear factura'
    titulo_actualizacion = None
    url_borrado = None
    success_url_name = 'factura_update'
    success_message = "Factura '{object}' creada correctamente."


# UD4.2.a: Permite modificar los datos de una factura existente.
class FacturaUpdateView(
    CreateUpdateSuccessMixin,
    CreateUpdateContextMixin,
    UpdateView,
):
    model = Factura
    # Reutiliza los mismos campos y la misma validación que la creación.
    form_class = FacturaForm
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar factura'
    url_borrado = 'factura_delete'
    success_url_name = 'factura_update'
    success_message = "Factura '{object}' actualizada correctamente."


# UD4.2.a: Solicita confirmación antes de eliminar una factura.
class FacturaDeleteView(ProtectedDeleteMixin, DeleteContextMixin, DeleteView):
    model = Factura
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar factura'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar la factura {object}?'
    )
    success_url = reverse_lazy('factura_list')


# UD3.7.a: Muestra el listado completo de cobros.
class CobroListView(OrderingMixin, ListView):
    model = Cobro
    template_name = 'billing/cobro_list.html'
    paginate_by = 5


# UD3.7.a: Muestra los datos de un cobro concreto.
class CobroDetailView(DetailView):
    model = Cobro
    template_name = 'billing/cobro_detail.html'


# UD4.2.a: Permite crear cobros mediante el formulario generado por Django.
class CobroCreateView(
    CobroMixin,
    CreateUpdateSuccessMixin,
    CreateUpdateContextMixin,
    CreateView,
):
    model = Cobro
    # El formulario valida el importe y el mixin comprueba el acumulado.
    form_class = CobroForm
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear cobro'
    titulo_actualizacion = None
    url_borrado = None
    success_url_name = 'cobro_update'
    success_message = "Cobro '{object}' creado correctamente."


# UD4.2.a: Permite modificar los datos de un cobro existente.
class CobroUpdateView(
    CobroMixin,
    CreateUpdateSuccessMixin,
    CreateUpdateContextMixin,
    UpdateView,
):
    model = Cobro
    # Reutiliza las mismas dos capas de validación que la creación.
    form_class = CobroForm
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar cobro'
    url_borrado = 'cobro_delete'
    success_url_name = 'cobro_update'
    success_message = "Cobro '{object}' actualizado correctamente."


# UD4.2.a: Solicita confirmación antes de eliminar un cobro.
class CobroDeleteView(ProtectedDeleteMixin, DeleteContextMixin, DeleteView):
    model = Cobro
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar cobro'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar el cobro {object}?'
    )
    success_url = reverse_lazy('cobro_list')
