from django.contrib import admin

from .models import Cliente, Factura, Cobro


# UD3.4.b: Configura la gestión de clientes en el administrador.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'nif', 'email')  # UD3.4.a: Columnas visibles.
    list_display_links = ('nombre', 'apellidos', 'nif', 'email')  # UD3.4.a: Campos que abren la edición.
    list_filter = ('nif',)  # UD3.4.a: Filtros de la barra lateral.
    search_fields = ('nombre', 'apellidos', 'nif', 'email')  # UD3.4.a: Campos donde busca el buscador.
    preserve_filters = True  # UD3.4.a: Conserva los filtros al volver a la lista.

# UD3.4.b: Configura la gestión de facturas según el anexo II.
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fecha', 'total')
    list_display_links = ('numero', 'fecha', 'total')
    list_filter = ('cliente',)
    search_fields = (
        'numero',
        'cliente__nombre',
        'cliente__apellidos',
    )
    preserve_filters = True

# UD3.4.b: Configura la gestión de cobros según el anexo II corregido.
@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'fecha', 'importe')
    list_display_links = ('numero_factura', 'fecha', 'importe')
    list_filter = ('factura__cliente',)
    search_fields = (
        'factura__numero',
        'factura__cliente__nombre',
        'factura__cliente__apellidos',
    )
    preserve_filters = True

    # Muestra el número de factura asociado al cobro.
    @admin.display(
        description='N.º factura',
        ordering='factura__numero',
    )
    def numero_factura(self, cobro):
        return cobro.factura.numero