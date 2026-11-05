from django.contrib import admin

from .models import CategoriaServicio, Servicio, Peluquero, HorarioSemanal, ExcepcionHorario, Reserva


# UD3.4.c: Permite gestionar las categorías de servicios.
@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    list_display_links = ('nombre',)
    # Busca tanto por el nombre como por el texto de la descripción.
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
    # Permite filtrar por categoría y por servicios activos o inactivos.
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'descripcion')
    preserve_filters = True

# UD3.4.c: Permite gestionar los peluqueros y sus servicios.
@admin.register(Peluquero)
class PeluqueroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'email', 'telefono', 'activo')
    list_display_links = ('nombre', 'apellidos')
    # Filtra por estado y por los servicios de la relación muchos a muchos.
    list_filter = ('activo', 'servicios')
    search_fields = ('nombre', 'apellidos', 'email', 'telefono')
    preserve_filters = True
    # Muestra dos listas para asignar varios servicios con más comodidad.
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
    # Combina filtros para localizar los bloques de trabajo necesarios.
    list_filter = ('peluquero', 'dia_semana', 'activo')
    # Busca por datos del peluquero relacionado, no por campos del horario.
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
    # Permite distinguir cierres y horarios especiales por fecha y peluquero.
    list_filter = ('peluquero', 'cerrado', 'fecha')
    # Combina datos del peluquero relacionado con el motivo de la excepción.
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
    # Permite revisar la agenda por profesional, estado o fecha de inicio.
    list_filter = ('peluquero', 'estado', 'fecha_inicio')
    # Busca atravesando las relaciones con Cliente y Peluquero.
    search_fields = (
        'cliente__nombre',
        'cliente__apellidos',
        'peluquero__nombre',
        'peluquero__apellidos',
    )
    preserve_filters = True
    # Facilita asignar varios servicios a la relación muchos a muchos.
    filter_horizontal = ('servicios',)
    # La fecha se genera sola y se muestra sin permitir cambios manuales.
    readonly_fields = ('fecha_creacion',)  # UD3.4.a: Muestra el campo sin permitir editarlo.
