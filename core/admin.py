from django.contrib import admin

from .models import CategoriaServicio, Servicio, Peluquero, HorarioSemanal, ExcepcionHorario, Reserva


# UD3.4.c: Permite gestionar las categorías de servicios.
@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    list_display_links = ('nombre',)
    search_fields = ('nombre', 'descripcion')
    preserve_filters = True

# UD3.4.c: Permite gestionar los servicios ofrecidos por la peluquería.
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'categoria',
        'duracion_minutos',
        'precio',
        'activo',
    )
    list_display_links = ('nombre',)
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'descripcion')
    preserve_filters = True

# UD3.4.c: Permite gestionar los peluqueros y sus servicios.
@admin.register(Peluquero)
class PeluqueroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'email', 'telefono', 'activo')
    list_display_links = ('nombre', 'apellidos')
    #Filtra por los peluqueros que ofrecen los servicios seleccionados.
    list_filter = ('activo', 'servicios')
    search_fields = ('nombre', 'apellidos', 'email', 'telefono')
    preserve_filters = True
    filter_horizontal = ('servicios',)  # UD3.4.a: Facilita seleccionar relaciones muchos-a-muchos.

# UD3.4.c: Permite gestionar los turnos semanales de cada peluquero.
@admin.register(HorarioSemanal)
class HorarioSemanalAdmin(admin.ModelAdmin):
    list_display = (
        'peluquero',
        'dia_semana',
        'hora_inicio',
        'hora_fin',
        'activo',
    )
    list_display_links = ('peluquero', 'dia_semana')
    list_filter = ('peluquero', 'dia_semana', 'activo')
    search_fields = ('peluquero__nombre', 'peluquero__apellidos')
    preserve_filters = True

# UD3.4.c: Permite gestionar cambios de horario para fechas concretas.
@admin.register(ExcepcionHorario)
class ExcepcionHorarioAdmin(admin.ModelAdmin):
    list_display = (
        'peluquero',
        'fecha',
        'cerrado',
        'hora_inicio',
        'hora_fin',
        'motivo',
    )
    list_display_links = ('peluquero', 'fecha')
    list_filter = ('peluquero', 'cerrado', 'fecha')
    search_fields = (
        'peluquero__nombre',
        'peluquero__apellidos',
        'motivo',
    )
    preserve_filters = True

# UD3.4.c: Permite consultar y gestionar las reservas.
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'peluquero',
        'fecha_inicio',
        'fecha_fin',
        'precio_total',
        'estado',
    )
    list_display_links = ('id',)
    list_filter = ('peluquero', 'estado', 'fecha_inicio')
    search_fields = (
        'cliente__nombre',
        'cliente__apellidos',
        'peluquero__nombre',
        'peluquero__apellidos',
    )
    preserve_filters = True
    filter_horizontal = ('servicios',)
    readonly_fields = ('fecha_creacion',)  # UD3.4.a: Muestra el campo sin permitir editarlo.