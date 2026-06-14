from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .services import marcar_leidas


@login_required
def lista(request):
    """Centro de notificaciones (campana). Al abrirlo se marcan como leídas."""
    notificaciones = list(request.user.notificaciones.all()[:50])
    marcar_leidas(request.user)
    return render(request, "notificaciones/lista.html", {"notificaciones": notificaciones})


@login_required
def marcar_todas_leidas(request):
    if request.method == "POST":
        marcar_leidas(request.user)
    return redirect("notificaciones:lista")
