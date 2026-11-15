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
    DeleteContextMixin,
    OrderingMixin,
    ProtectedDeleteMixin,
)

from .mixins import ReservaMixin
from .models import (
    CategoriaServicio,
    ExcepcionHorario,
    HorarioSemanal,
    Peluquero,
    Reserva,
    Servicio,
)

# UD4.2: Todas las vistas nuevas reutilizan los mismos patrones: el mixin se
# coloca antes de la CBV, fields expone solo datos editables, los valores
# derivados de Reserva quedan fuera y cada borrado regresa a su propio listado.

# UD3.7.a: Muestra todas las categorías de servicios.
class CategoriaServicioListView(OrderingMixin, ListView):
    model = CategoriaServicio
    template_name = 'core/categoria_servicio_list.html'
    paginate_by = 5


# UD3.7.a: Muestra una categoría de servicio mediante su PK.
class CategoriaServicioDetailView(DetailView):
    model = CategoriaServicio
    template_name = 'core/categoria_servicio_detail.html'
    context_object_name = 'categoria_servicio'


# UD4.2.a: Permite crear categorías mediante el formulario generado por Django.
class CategoriaServicioCreateView(CreateUpdateContextMixin, CreateView):
    model = CategoriaServicio
    fields = [
        'nombre',
        'descripcion',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear categoría de servicio'
    titulo_actualizacion = None
    url_borrado = None


# UD4.2.a: Permite modificar una categoría existente.
class CategoriaServicioUpdateView(CreateUpdateContextMixin, UpdateView):
    model = CategoriaServicio
    fields = [
        'nombre',
        'descripcion',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar categoría de servicio'
    url_borrado = 'categoria_servicio_delete'


# UD4.2.a: Solicita confirmación antes de eliminar una categoría.
class CategoriaServicioDeleteView(
    ProtectedDeleteMixin,
    DeleteContextMixin,
    DeleteView,
):
    model = CategoriaServicio
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar categoría de servicio'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar la categoría {object}?'
    )
    success_url = reverse_lazy('categoria_servicio_list')


# UD3.7.a: Muestra todos los servicios.
class ServicioListView(OrderingMixin, ListView):
    model = Servicio
    template_name = 'core/servicio_list.html'
    paginate_by = 5


# UD3.7.a: Muestra un servicio mediante su PK.
class ServicioDetailView(DetailView):
    model = Servicio
    template_name = 'core/servicio_detail.html'


# UD4.2.a: Permite crear servicios mediante el formulario generado por Django.
class ServicioCreateView(CreateUpdateContextMixin, CreateView):
    model = Servicio
    fields = [
        'categoria',
        'nombre',
        'descripcion',
        'duracion_minutos',
        'precio',
        'activo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear servicio'
    titulo_actualizacion = None
    url_borrado = None


# UD4.2.a: Permite modificar un servicio existente.
class ServicioUpdateView(CreateUpdateContextMixin, UpdateView):
    model = Servicio
    fields = [
        'categoria',
        'nombre',
        'descripcion',
        'duracion_minutos',
        'precio',
        'activo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar servicio'
    url_borrado = 'servicio_delete'


# UD4.2.a: Solicita confirmación antes de eliminar un servicio.
class ServicioDeleteView(ProtectedDeleteMixin, DeleteContextMixin, DeleteView):
    model = Servicio
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar servicio'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar el servicio {object}?'
    )
    success_url = reverse_lazy('servicio_list')


# UD3.7.a: Muestra todos los peluqueros.
class PeluqueroListView(OrderingMixin, ListView):
    model = Peluquero
    template_name = 'core/peluquero_list.html'
    paginate_by = 5


# UD3.7.a: Muestra un peluquero mediante su PK.
class PeluqueroDetailView(DetailView):
    model = Peluquero
    template_name = 'core/peluquero_detail.html'


# UD4.2.a: Permite crear peluqueros mediante el formulario generado por Django.
class PeluqueroCreateView(CreateUpdateContextMixin, CreateView):
    model = Peluquero
    fields = [
        'nombre',
        'apellidos',
        'email',
        'telefono',
        'servicios',
        'activo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear peluquero'
    titulo_actualizacion = None
    url_borrado = None


# UD4.2.a: Permite modificar los datos de un peluquero existente.
class PeluqueroUpdateView(CreateUpdateContextMixin, UpdateView):
    model = Peluquero
    fields = [
        'nombre',
        'apellidos',
        'email',
        'telefono',
        'servicios',
        'activo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar peluquero'
    url_borrado = 'peluquero_delete'


# UD4.2.a: Solicita confirmación antes de eliminar un peluquero.
class PeluqueroDeleteView(ProtectedDeleteMixin, DeleteContextMixin, DeleteView):
    model = Peluquero
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar peluquero'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar al peluquero {object}?'
    )
    success_url = reverse_lazy('peluquero_list')


# UD3.7.a: Muestra todos los horarios semanales.
class HorarioSemanalListView(OrderingMixin, ListView):
    model = HorarioSemanal
    template_name = 'core/horario_semanal_list.html'
    paginate_by = 5


# UD3.7.a: Muestra un horario semanal mediante su PK.
class HorarioSemanalDetailView(DetailView):
    model = HorarioSemanal
    template_name = 'core/horario_semanal_detail.html'
    context_object_name = 'horario_semanal'


# UD4.2.a: Permite crear horarios semanales mediante el formulario de Django.
class HorarioSemanalCreateView(CreateUpdateContextMixin, CreateView):
    model = HorarioSemanal
    fields = [
        'peluquero',
        'dia_semana',
        'hora_inicio',
        'hora_fin',
        'activo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear horario semanal'
    titulo_actualizacion = None
    url_borrado = None


# UD4.2.a: Permite modificar un horario semanal existente.
class HorarioSemanalUpdateView(CreateUpdateContextMixin, UpdateView):
    model = HorarioSemanal
    fields = [
        'peluquero',
        'dia_semana',
        'hora_inicio',
        'hora_fin',
        'activo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar horario semanal'
    url_borrado = 'horario_semanal_delete'


# UD4.2.a: Solicita confirmación antes de eliminar un horario semanal.
class HorarioSemanalDeleteView(
    ProtectedDeleteMixin,
    DeleteContextMixin,
    DeleteView,
):
    model = HorarioSemanal
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar horario semanal'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar el horario {object}?'
    )
    success_url = reverse_lazy('horario_semanal_list')


# UD3.7.a: Muestra todas las excepciones de horario.
class ExcepcionHorarioListView(OrderingMixin, ListView):
    model = ExcepcionHorario
    template_name = 'core/excepcion_horario_list.html'
    paginate_by = 5


# UD3.7.a: Muestra una excepción de horario mediante su PK.
class ExcepcionHorarioDetailView(DetailView):
    model = ExcepcionHorario
    template_name = 'core/excepcion_horario_detail.html'
    context_object_name = 'excepcion_horario'


# UD4.2.a: Permite crear excepciones de horario con el formulario de Django.
class ExcepcionHorarioCreateView(CreateUpdateContextMixin, CreateView):
    model = ExcepcionHorario
    fields = [
        'peluquero',
        'fecha',
        'hora_inicio',
        'hora_fin',
        'cerrado',
        'motivo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear excepción de horario'
    titulo_actualizacion = None
    url_borrado = None


# UD4.2.a: Permite modificar una excepción de horario existente.
class ExcepcionHorarioUpdateView(CreateUpdateContextMixin, UpdateView):
    model = ExcepcionHorario
    fields = [
        'peluquero',
        'fecha',
        'hora_inicio',
        'hora_fin',
        'cerrado',
        'motivo',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar excepción de horario'
    url_borrado = 'excepcion_horario_delete'


# UD4.2.a: Solicita confirmación antes de eliminar una excepción de horario.
class ExcepcionHorarioDeleteView(
    ProtectedDeleteMixin,
    DeleteContextMixin,
    DeleteView,
):
    model = ExcepcionHorario
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar excepción de horario'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar la excepción {object}?'
    )
    success_url = reverse_lazy('excepcion_horario_list')


# UD3.7.a: Muestra todas las reservas.
class ReservaListView(OrderingMixin, ListView):
    model = Reserva
    template_name = 'core/reserva_list.html'
    paginate_by = 5


# UD3.7.a: Muestra una reserva mediante su PK.
class ReservaDetailView(DetailView):
    model = Reserva
    template_name = 'core/reserva_detail.html'


# UD4.2.a: Crea reservas solicitando únicamente los datos elegidos por el usuario.
class ReservaCreateView(
    ReservaMixin,
    CreateUpdateContextMixin,
    CreateView,
):
    model = Reserva
    fields = [
        'cliente',
        'peluquero',
        'servicios',
        'fecha_inicio',
        'estado',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = 'Crear reserva'
    titulo_actualizacion = None
    url_borrado = None


# UD4.2.a: Actualiza una reserva y vuelve a calcular sus valores derivados.
class ReservaUpdateView(
    ReservaMixin,
    CreateUpdateContextMixin,
    UpdateView,
):
    model = Reserva
    fields = [
        'cliente',
        'peluquero',
        'servicios',
        'fecha_inicio',
        'estado',
    ]
    template_name = 'common/base_create_update.html'
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar reserva'
    url_borrado = 'reserva_delete'


# UD4.2.a: Solicita confirmación antes de eliminar una reserva.
class ReservaDeleteView(ProtectedDeleteMixin, DeleteContextMixin, DeleteView):
    model = Reserva
    template_name = 'common/base_confirm_delete.html'
    titulo = 'Eliminar reserva'
    mensaje_confirmacion = (
        '¿Está seguro de que desea eliminar la reserva {object}?'
    )
    success_url = reverse_lazy('reserva_list')
