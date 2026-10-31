from django.views.generic import DetailView, ListView

from .models import Cliente, Factura, Cobro


# UD3.7.a: Muestra el listado de clientes.
class ClienteListView(ListView):
    model = Cliente
    template_name = 'billing/cliente_list.html'
    paginate_by = 5


# UD3.7.a: Muestra los datos de un cliente concreto.
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'billing/cliente_detail.html'

# UD3.7.a: Muestra el listado completo de facturas.
class FacturaListView(ListView):
    model = Factura
    template_name = 'billing/factura_list.html'
    paginate_by = 5

# UD3.7.a: Muestra los datos de una factura concreta.
class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'billing/factura_detail.html'

# UD3.7.a: Muestra el listado completo de cobros.
class CobroListView(ListView):
    model = Cobro
    template_name = 'billing/cobro_list.html'
    paginate_by = 5


# UD3.7.a: Muestra los datos de un cobro concreto.
class CobroDetailView(DetailView):
    model = Cobro
    template_name = 'billing/cobro_detail.html'