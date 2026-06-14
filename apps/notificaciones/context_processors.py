"""Expone el contador y las últimas notificaciones a las plantillas (campana)."""

from .services import no_leidas


def notificaciones(request):
    if not request.user.is_authenticated:
        return {"notificaciones_no_leidas": 0, "notificaciones_recientes": []}
    return {
        "notificaciones_no_leidas": no_leidas(request.user),
        "notificaciones_recientes": list(request.user.notificaciones.all()[:5]),
    }
