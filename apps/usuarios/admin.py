from django.contrib import admin

from .models import Credencial, Perfil, PerfilTalento


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "rol", "consentimiento_datos", "perfil_completo", "creado_en")
    list_filter = ("rol", "consentimiento_datos", "perfil_completo")
    search_fields = ("user__username", "user__email")


class CredencialInline(admin.TabularInline):
    model = Credencial
    extra = 0


@admin.register(PerfilTalento)
class PerfilTalentoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "carrera", "estado_academico", "cred_activa", "cred_slug")
    list_filter = ("estado_academico", "cred_activa")
    search_fields = ("usuario__username", "usuario__email")
    inlines = [CredencialInline]


@admin.register(Credencial)
class CredencialAdmin(admin.ModelAdmin):
    list_display = ("perfil", "tipo", "detalle", "fuente", "visible_para_empresas")
    list_filter = ("tipo", "fuente", "visible_para_empresas")
