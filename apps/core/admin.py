from django.contrib import admin

from .models import AdminAllowlist, ParametroLegal, PesoTransparencia, ReglaElegibilidad


@admin.register(ParametroLegal)
class ParametroLegalAdmin(admin.ModelAdmin):
    list_display = ("clave", "valor", "descripcion", "actualizado_en")
    search_fields = ("clave", "descripcion")


@admin.register(PesoTransparencia)
class PesoTransparenciaAdmin(admin.ModelAdmin):
    list_display = ("criterio", "etiqueta", "peso")
    list_editable = ("peso",)


@admin.register(ReglaElegibilidad)
class ReglaElegibilidadAdmin(admin.ModelAdmin):
    list_display = ("estado_academico", "tipo_convocatoria", "permitido")
    list_filter = ("estado_academico", "tipo_convocatoria", "permitido")
    list_editable = ("permitido",)


@admin.register(AdminAllowlist)
class AdminAllowlistAdmin(admin.ModelAdmin):
    list_display = ("email", "nota", "creado_en")
    search_fields = ("email",)
