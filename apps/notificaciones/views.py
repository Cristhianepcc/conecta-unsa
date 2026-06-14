from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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
def marcar_todas_leidas(request):
    if request.method == "POST":
        marcar_leidas(request.user)
    return redirect("notificaciones:lista")
