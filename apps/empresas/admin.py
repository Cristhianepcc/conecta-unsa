from django.contrib import admin

from .models import Empresa, Reclutador
from .services import activar_empresa, rechazar_empresa


class ReclutadorInline(admin.StackedInline):
    model = Reclutador
    extra = 0
    autocomplete_fields = ("usuario",)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "ruc", "estado", "_verificada", "_referencial")
    list_filter = ("estado", "tipo")
    search_fields = ("razon_social", "nombre_comercial", "ruc")
    inlines = [ReclutadorInline]
    actions = ["accion_activar", "accion_rechazar"]

    @admin.display(boolean=True, description="verificada")
    def _verificada(self, obj):
        return obj.verificada

    @admin.display(boolean=True, description="referencial")
    def _referencial(self, obj):
        return obj.es_referencial

    @admin.action(description="Activar empresas seleccionadas")
    def accion_activar(self, request, queryset):
        for empresa in queryset:
            activar_empresa(empresa)
        self.message_user(request, f"{queryset.count()} empresa(s) activada(s).")

    @admin.action(description="Rechazar empresas seleccionadas")
    def accion_rechazar(self, request, queryset):
        for empresa in queryset:
            rechazar_empresa(empresa)
        self.message_user(request, f"{queryset.count()} empresa(s) rechazada(s).")


@admin.register(Reclutador)
class ReclutadorAdmin(admin.ModelAdmin):
    list_display = ("nombres", "ap_paterno", "empresa", "cargo", "email")
    search_fields = ("nombres", "ap_paterno", "empresa__razon_social")
    autocomplete_fields = ("usuario", "empresa")
