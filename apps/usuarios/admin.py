from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "rol", "consentimiento_datos", "perfil_completo", "creado_en")
    list_filter = ("rol", "consentimiento_datos", "perfil_completo")
    search_fields = ("user__username", "user__email")
