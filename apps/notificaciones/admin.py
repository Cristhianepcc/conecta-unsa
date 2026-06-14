from django.contrib import admin

from .models import Notificacion, ResumenSemanalLog


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo", "mensaje", "leido", "creado_en")
    list_filter = ("tipo", "leido")
    search_fields = ("usuario__username", "usuario__email", "mensaje")


@admin.register(ResumenSemanalLog)
class ResumenSemanalLogAdmin(admin.ModelAdmin):
    list_display = ("usuario", "enviado_en", "_n")
    search_fields = ("usuario__username", "usuario__email")

    @admin.display(description="n.º convocatorias")
    def _n(self, obj):
        return obj.convocatorias.count()
