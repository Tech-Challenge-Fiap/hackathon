from django.contrib import admin
from .models import PerfilUsuario, Clinica

class AdminPerfilUsuario(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_usuario')

class AdminClinica(admin.ModelAdmin):
    list_display = ("nome", "endereco", "longitude", "latitude")

admin.site.register(PerfilUsuario, AdminPerfilUsuario)
admin.site.register(Clinica, AdminClinica)
