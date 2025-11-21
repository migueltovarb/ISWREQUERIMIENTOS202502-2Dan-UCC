# core/admin.py
from django.contrib import admin
from .models import Laboratorio, Equipo, Reserva, PerfilUsuario

# Registramos los modelos que NO van a tener configuración especial
admin.site.register(Equipo)
admin.site.register(Reserva)
admin.site.register(PerfilUsuario)

# Solo Laboratorio lo registramos con la clase bonita (una sola vez)
@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)