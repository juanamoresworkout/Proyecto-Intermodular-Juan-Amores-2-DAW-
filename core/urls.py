from django.urls import path

from .views import (
    CategoriaServicioDetailView, CategoriaServicioListView,
    ExcepcionHorarioDetailView, ExcepcionHorarioListView,
    HorarioSemanalDetailView, HorarioSemanalListView,
    PeluqueroDetailView, PeluqueroListView,
    ReservaDetailView, ReservaListView,
    ServicioDetailView, ServicioListView,
)

urlpatterns = [
    # UD3.7.b: Rutas de lista y detalle de los modelos de core.
    path('categorias/', CategoriaServicioListView.as_view(), name='categoria_servicio_list'),
    path('categorias/<int:pk>/', CategoriaServicioDetailView.as_view(), name='categoria_servicio_detail'),
    path('servicios/', ServicioListView.as_view(), name='servicio_list'),
    path('servicios/<int:pk>/', ServicioDetailView.as_view(), name='servicio_detail'),
    path('peluqueros/', PeluqueroListView.as_view(), name='peluquero_list'),
    path('peluqueros/<int:pk>/', PeluqueroDetailView.as_view(), name='peluquero_detail'),
    path('horarios/', HorarioSemanalListView.as_view(), name='horario_semanal_list'),
    path('horarios/<int:pk>/', HorarioSemanalDetailView.as_view(), name='horario_semanal_detail'),
    path('excepciones/', ExcepcionHorarioListView.as_view(), name='excepcion_horario_list'),
    path('excepciones/<int:pk>/', ExcepcionHorarioDetailView.as_view(), name='excepcion_horario_detail'),
    path('reservas/', ReservaListView.as_view(), name='reserva_list'),
    path('reservas/<int:pk>/', ReservaDetailView.as_view(), name='reserva_detail'),
]
