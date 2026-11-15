from django.urls import path

from .views import *

urlpatterns = [
    # UD3.7.b: Rutas para listar clientes y consultar uno mediante su PK.
    path(
        'cliente_list/', 
        ClienteListView.as_view(), 
        name='cliente_list'
    ),
    path(
        'cliente_detail/<int:pk>/',
        ClienteDetailView.as_view(),
        name='cliente_detail',
    ),

    # UD4.2.b: Rutas para crear, actualizar y eliminar clientes.
    path(
        'cliente_create/',
        ClienteCreateView.as_view(),
        name='cliente_create',
    ),
    path(
        'cliente_update/<int:pk>/',
        ClienteUpdateView.as_view(),
        name='cliente_update',
    ),
    path(
        'cliente_delete/<int:pk>/',
        ClienteDeleteView.as_view(),
        name='cliente_delete',
    ),

    # UD3.7.b: Rutas para listar facturas y consultar una mediante su PK.
    path(
        'factura_list/',
        FacturaListView.as_view(), 
        name='factura_list'
    ),

    path(
        'factura_detail/<int:pk>/',
        FacturaDetailView.as_view(),
        name='factura_detail',
    ),

    # UD4.2.b: Rutas para crear, actualizar y eliminar facturas.
    path(
        'factura_create/',
        FacturaCreateView.as_view(),
        name='factura_create',
    ),
    path(
        'factura_update/<int:pk>/',
        FacturaUpdateView.as_view(),
        name='factura_update',
    ),
    path(
        'factura_delete/<int:pk>/',
        FacturaDeleteView.as_view(),
        name='factura_delete',
    ),

    # UD3.7.b: Rutas para listar cobros y consultar uno mediante su PK.
    path(
        'cobro_list/', 
        CobroListView.as_view(), 
        name='cobro_list'
    ),
    
    path(
        'cobro_detail/<int:pk>/',
        CobroDetailView.as_view(),
        name='cobro_detail',
    ),

    # UD4.2.b: Rutas para crear, actualizar y eliminar cobros.
    path(
        'cobro_create/',
        CobroCreateView.as_view(),
        name='cobro_create',
    ),
    path(
        'cobro_update/<int:pk>/',
        CobroUpdateView.as_view(),
        name='cobro_update',
    ),
    path(
        'cobro_delete/<int:pk>/',
        CobroDeleteView.as_view(),
        name='cobro_delete',
    ),
]
