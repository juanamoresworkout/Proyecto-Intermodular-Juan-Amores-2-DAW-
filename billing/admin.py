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
    # Permite limitar el listado a las facturas de un cliente concreto.
    list_filter = ('cliente',)
    # Además del número, busca datos atravesando la relación con Cliente.
    search_fields = (
        'numero',
        'cliente__nombre',
        'cliente__apellidos',
    )
    preserve_filters = True

# UD3.4.b: Configura la gestión de cobros según el anexo II corregido.
@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    # numero_factura es un método de esta clase, no un campo de Cobro.
    list_display = ('numero_factura', 'fecha', 'importe')
    list_display_links = ('numero_factura', 'fecha', 'importe')
    # Llega al cliente pasando primero por la factura del cobro.
    list_filter = ('factura__cliente',)
    # Permite buscar por la factura y por su cliente relacionado.
    search_fields = (
        'factura__numero',
        'factura__cliente__nombre',
        'factura__cliente__apellidos',
    )
    preserve_filters = True

    # Muestra el número de factura asociado al cobro.
    @admin.display(
        # Texto que aparece en la cabecera de la columna calculada.
        description='N.º factura',
        # Campo real que Django usa al ordenar esta columna.
        ordering='factura__numero',
    )
    def numero_factura(self, cobro):
        # Desde el cobro accede a su factura y devuelve solo su número.
        return cobro.factura.numero
