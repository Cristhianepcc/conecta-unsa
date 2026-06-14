"""Expone el contador de notificaciones no leídas a todas las plantillas (campana 🔔)."""

from .services import no_leidas


def notificaciones(request):
    if request.user.is_authenticated:
        return {"notificaciones_no_leidas": no_leidas(request.user)}
    return {"notificaciones_no_leidas": 0}
