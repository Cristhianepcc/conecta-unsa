from django.contrib import admin

from .models import Convocatoria


@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo", "empresa", "tipo", "estado", "transparencia_pct", "creada_por", "creada_en"
    )
    list_filter = ("estado", "tipo", "creada_por", "modalidad")
    search_fields = ("titulo", "empresa__razon_social")
    autocomplete_fields = ("empresa",)
    filter_horizontal = ("carreras_objetivo",)
    readonly_fields = ("transparencia_pct", "creada_en", "actualizada_en")
    fieldsets = (
        ("Origen", {"fields": ("empresa", "creada_por", "tipo", "estado")}),
        ("Nivel 1 — Fundamentales", {
            "fields": ("titulo", "descripcion", "modalidad", "ubicacion",
                       "duracion_estimada", "fecha_limite", "medio_postulacion",
                       "email_contacto", "no_discriminacion", "carreras_objetivo"),
        }),
        ("Nivel 2 — Según tipo", {
            "classes": ("collapse",),
            "fields": ("subvencion_remuneracion", "jornada_horas", "requiere_convenio",
                       "ciclo_minimo", "tiempo_egreso_meses", "regimen", "bases_url",
                       "cronograma", "entidad_otorgante", "no_vinculo", "incluye_seguro"),
        }),
        ("Nivel 3 — Opcionales", {
            "classes": ("collapse",),
            "fields": ("banda_salarial_min", "banda_salarial_max", "salario_confidencial",
                       "vacantes", "beneficios", "discapacidad"),
        }),
        ("Calculado", {"fields": ("transparencia_pct", "creada_en", "actualizada_en")}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.recalcular_transparencia()
