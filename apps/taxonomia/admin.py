from django.contrib import admin

from .models import Area, Carrera, Facultad, GrupoAfin


class CarreraInline(admin.TabularInline):
    model = Carrera
    extra = 0
    fields = ("nombre", "activa")


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "orden")
    list_editable = ("orden",)


@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "area")
    list_filter = ("area",)
    search_fields = ("nombre",)
    inlines = [CarreraInline]


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ("nombre", "facultad", "activa")
    list_filter = ("activa", "facultad__area", "facultad")
    search_fields = ("nombre",)
    list_editable = ("activa",)


@admin.register(GrupoAfin)
class GrupoAfinAdmin(admin.ModelAdmin):
    list_display = ("nombre", "_n_carreras")
    search_fields = ("nombre",)
    filter_horizontal = ("carreras",)

    @admin.display(description="n.º carreras")
    def _n_carreras(self, obj):
        return obj.carreras.count()
