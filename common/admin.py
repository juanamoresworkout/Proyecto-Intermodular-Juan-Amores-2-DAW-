from django.contrib import admin

from .models import DiaSemana, EstadoReserva


# UD3.4.c: Permite consultar los días disponibles para los horarios.
@admin.register(DiaSemana)
class DiaSemanaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    list_display_links = ('codigo', 'nombre')
    ordering = ('codigo',)


# UD3.4.c: Permite consultar los estados disponibles para las reservas.
@admin.register(EstadoReserva)
class EstadoReservaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    list_display_links = ('codigo', 'nombre')
    ordering = ('nombre',)
