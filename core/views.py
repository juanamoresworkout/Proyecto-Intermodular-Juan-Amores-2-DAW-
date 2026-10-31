from django.views.generic import DetailView, ListView

from .models import (
    CategoriaServicio,
    ExcepcionHorario,
    HorarioSemanal,
    Peluquero,
    Reserva,
    Servicio,
)


# UD3.7.a: Muestra todas las categorías de servicios.
class CategoriaServicioListView(ListView):
    model = CategoriaServicio
    template_name = 'core/categoria_servicio_list.html'
    paginate_by = 5


# UD3.7.a: Muestra una categoría de servicio mediante su PK.
class CategoriaServicioDetailView(DetailView):
    model = CategoriaServicio
    template_name = 'core/categoria_servicio_detail.html'
    context_object_name = 'categoria_servicio'


# UD3.7.a: Muestra todos los servicios.
class ServicioListView(ListView):
    model = Servicio
    template_name = 'core/servicio_list.html'
    paginate_by = 5


# UD3.7.a: Muestra un servicio mediante su PK.
class ServicioDetailView(DetailView):
    model = Servicio
    template_name = 'core/servicio_detail.html'


# UD3.7.a: Muestra todos los peluqueros.
class PeluqueroListView(ListView):
    model = Peluquero
    template_name = 'core/peluquero_list.html'
    paginate_by = 5


# UD3.7.a: Muestra un peluquero mediante su PK.
class PeluqueroDetailView(DetailView):
    model = Peluquero
    template_name = 'core/peluquero_detail.html'


# UD3.7.a: Muestra todos los horarios semanales.
class HorarioSemanalListView(ListView):
    model = HorarioSemanal
    template_name = 'core/horario_semanal_list.html'
    paginate_by = 5


# UD3.7.a: Muestra un horario semanal mediante su PK.
class HorarioSemanalDetailView(DetailView):
    model = HorarioSemanal
    template_name = 'core/horario_semanal_detail.html'
    context_object_name = 'horario_semanal'


# UD3.7.a: Muestra todas las excepciones de horario.
class ExcepcionHorarioListView(ListView):
    model = ExcepcionHorario
    template_name = 'core/excepcion_horario_list.html'
    paginate_by = 5


# UD3.7.a: Muestra una excepción de horario mediante su PK.
class ExcepcionHorarioDetailView(DetailView):
    model = ExcepcionHorario
    template_name = 'core/excepcion_horario_detail.html'
    context_object_name = 'excepcion_horario'


# UD3.7.a: Muestra todas las reservas.
class ReservaListView(ListView):
    model = Reserva
    template_name = 'core/reserva_list.html'
    paginate_by = 5


# UD3.7.a: Muestra una reserva mediante su PK.
class ReservaDetailView(DetailView):
    model = Reserva
    template_name = 'core/reserva_detail.html'
