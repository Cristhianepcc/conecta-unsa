"""Expone el contador y las últimas notificaciones a las plantillas (campana)."""

from .models import TIPO_GENERAL
from .services import no_leidas


def notificaciones(request):
    if not request.user.is_authenticated:
        return {
            "notificaciones_no_leidas": 0,
            "notificaciones_recientes": [],
            "mensajes_no_leidos": 0,
        }
    return {
        "notificaciones_no_leidas": no_leidas(request.user),
        "notificaciones_recientes": list(request.user.notificaciones.all()[:5]),
        "mensajes_no_leidos": request.user.notificaciones.filter(
            tipo=TIPO_GENERAL, leido=False
        ).count(),
    }
