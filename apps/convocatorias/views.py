from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.matching.services import puntuar

from .interacciones import alternar_guardada, esta_guardada, registrar_vista
from .models import ESTADO_PUBLICADA, Convocatoria


@login_required
def detalle(request, pk):
    """Detalle de la convocatoria; registra la vista (CA-3)."""
    conv = get_object_or_404(Convocatoria, pk=pk)
    registrar_vista(request.user, conv)
    _puntaje, motivos = puntuar(request.user, conv)
    return render(
        request,
        "convocatorias/detalle.html",
        {"conv": conv, "motivos": motivos, "guardada": esta_guardada(request.user, conv)},
    )


@login_required
def postular(request, pk):
    """Registra la vista y redirige al medio de postulación externo (CA-3).

    La plataforma no gestiona la selección (decisión de la propuesta).
    """
    conv = get_object_or_404(Convocatoria, pk=pk, estado=ESTADO_PUBLICADA)
    registrar_vista(request.user, conv)
    destino = conv.medio_postulacion
    if not destino:
        return redirect("convocatorias:detalle", pk=pk)
    if "@" in destino and not destino.startswith("http"):
        destino = f"mailto:{destino}"
    return redirect(destino)


@login_required
@require_http_methods(["POST"])
def guardar(request, pk):
    """Guarda o quita la convocatoria de guardadas (CA-4)."""
    conv = get_object_or_404(Convocatoria, pk=pk)
    alternar_guardada(request.user, conv)
    destino = request.POST.get("next")
    if destino:
        return redirect(destino)
    return redirect("convocatorias:detalle", pk=pk)
