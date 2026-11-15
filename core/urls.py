from django.urls import path

from .views import *


urlpatterns = [
    # UD3.7.b: Rutas de lista y detalle de los modelos de core.
    path('categorias/', CategoriaServicioListView.as_view(), name='categoria_servicio_list'),
    path('categorias/<int:pk>/', CategoriaServicioDetailView.as_view(), name='categoria_servicio_detail'),
    # UD4.2.b: Rutas para crear, actualizar y eliminar categorías.
    path('categorias/create/', CategoriaServicioCreateView.as_view(), name='categoria_servicio_create'),
    path('categorias/<int:pk>/update/', CategoriaServicioUpdateView.as_view(), name='categoria_servicio_update'),
    path('categorias/<int:pk>/delete/', CategoriaServicioDeleteView.as_view(), name='categoria_servicio_delete'),

    path('servicios/', ServicioListView.as_view(), name='servicio_list'),
    path('servicios/<int:pk>/', ServicioDetailView.as_view(), name='servicio_detail'),
    # UD4.2.b: Rutas para crear, actualizar y eliminar servicios.
    path('servicios/create/', ServicioCreateView.as_view(), name='servicio_create'),
    path('servicios/<int:pk>/update/', ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicios/<int:pk>/delete/', ServicioDeleteView.as_view(), name='servicio_delete'),

    path('peluqueros/', PeluqueroListView.as_view(), name='peluquero_list'),
    path('peluqueros/<int:pk>/', PeluqueroDetailView.as_view(), name='peluquero_detail'),
    # UD4.2.b: Rutas para crear, actualizar y eliminar peluqueros.
    path('peluqueros/create/', PeluqueroCreateView.as_view(), name='peluquero_create'),
    path('peluqueros/<int:pk>/update/', PeluqueroUpdateView.as_view(), name='peluquero_update'),
    path('peluqueros/<int:pk>/delete/', PeluqueroDeleteView.as_view(), name='peluquero_delete'),

    path('horarios/', HorarioSemanalListView.as_view(), name='horario_semanal_list'),
    path('horarios/<int:pk>/', HorarioSemanalDetailView.as_view(), name='horario_semanal_detail'),
    # UD4.2.b: Rutas para crear, actualizar y eliminar horarios semanales.
    path('horarios/create/', HorarioSemanalCreateView.as_view(), name='horario_semanal_create'),
    path('horarios/<int:pk>/update/', HorarioSemanalUpdateView.as_view(), name='horario_semanal_update'),
    path('horarios/<int:pk>/delete/', HorarioSemanalDeleteView.as_view(), name='horario_semanal_delete'),

    path('excepciones/', ExcepcionHorarioListView.as_view(), name='excepcion_horario_list'),
    path('excepciones/<int:pk>/', ExcepcionHorarioDetailView.as_view(), name='excepcion_horario_detail'),
    # UD4.2.b: Rutas para crear, actualizar y eliminar excepciones de horario.
    path('excepciones/create/', ExcepcionHorarioCreateView.as_view(), name='excepcion_horario_create'),
    path('excepciones/<int:pk>/update/', ExcepcionHorarioUpdateView.as_view(), name='excepcion_horario_update'),
    path('excepciones/<int:pk>/delete/', ExcepcionHorarioDeleteView.as_view(), name='excepcion_horario_delete'),

    path('reservas/', ReservaListView.as_view(), name='reserva_list'),
    path('reservas/<int:pk>/', ReservaDetailView.as_view(), name='reserva_detail'),
    # UD4.2.b: Rutas para crear, actualizar y eliminar reservas.
    path('reservas/create/', ReservaCreateView.as_view(), name='reserva_create'),
    path('reservas/<int:pk>/update/', ReservaUpdateView.as_view(), name='reserva_update'),
    path('reservas/<int:pk>/delete/', ReservaDeleteView.as_view(), name='reserva_delete'),
]
