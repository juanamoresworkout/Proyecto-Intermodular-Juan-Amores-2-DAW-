from django.urls import path 

from .views import ( ClienteDetailView,ClienteListView,CobroDetailView,CobroListView,FacturaDetailView,FacturaListView,)


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
]