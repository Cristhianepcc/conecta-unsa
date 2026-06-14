from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import TIPO_GENERAL
from .services import marcar_leidas


@login_required
def lista(request):
    """Centro de notificaciones (campana). Al abrirlo se marcan como leídas."""
    notificaciones = list(request.user.notificaciones.all()[:50])
    sin_leer = sum(1 for n in notificaciones if not n.leido)  # antes de marcar
    marcar_leidas(request.user)
    return render(
        request,
        "notificaciones/lista.html",
        {"notificaciones": notificaciones, "sin_leer": sin_leer},
    )


@login_required
def institucionales(request):
    """Bandeja de mensajes institucionales (comunicados oficiales de la UNSA).

    Canal dedicado, separado de las notificaciones operativas de la campana.
    """
    mensajes = list(request.user.notificaciones.filter(tipo=TIPO_GENERAL)[:50])
    sin_leer = sum(1 for m in mensajes if not m.leido)  # antes de marcar
    marcar_leidas(request.user, ids=[m.id for m in mensajes if not m.leido])
    return render(
        request,
        "notificaciones/institucionales.html",
        {"mensajes": mensajes, "sin_leer": sin_leer},
    )


@login_required
def marcar_todas_leidas(request):
    if request.method == "POST":
        marcar_leidas(request.user)
    return redirect("notificaciones:lista")
