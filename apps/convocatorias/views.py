from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods


class RedirectExterno(HttpResponseRedirect):
    """Redirección al medio de postulación: permite también mailto (Django bloquea mailto por defecto)."""

    allowed_schemes = ["http", "https", "mailto"]

from apps.matching.services import compatibilidad, puntuar

from .interacciones import alternar_guardada, esta_guardada, registrar_vista
from .models import ESTADO_PUBLICADA, Convocatoria


@login_required
def detalle(request, pk):
    """Detalle de la convocatoria; registra la vista (CA-3)."""
    conv = get_object_or_404(Convocatoria, pk=pk)
    registrar_vista(request.user, conv)
    _puntaje, motivos = puntuar(request.user, conv)
    match, chips = compatibilidad(request.user, conv)
    return render(
        request,
        "convocatorias/detalle.html",
        {
            "conv": conv,
            "motivos": motivos,
            "match": match,
            "chips": chips,
            "guardada": esta_guardada(request.user, conv),
        },
    )


@login_required
def postular(request, pk):
    """Registra la vista y redirige al medio de postulación externo (CA-3).

    La plataforma no gestiona la selección (decisión de la propuesta).
    """
    from urllib.parse import quote

    conv = get_object_or_404(Convocatoria, pk=pk, estado=ESTADO_PUBLICADA)
    registrar_vista(request.user, conv)
    if not conv.activa:  # vencida aunque el cron no la haya caducado (feature 13)
        return redirect("convocatorias:detalle", pk=pk)
    destino = conv.medio_efectivo
    if not destino:
        return redirect("convocatorias:detalle", pk=pk)
    if conv.medio_es_correo:
        # Caso común: la empresa solo deja un correo para enviar el CV.
        # Abrimos un borrador con el asunto pre-llenado (adjuntar CV lo hace el postulante).
        asunto = quote(f"Postulación: {conv.titulo} — {conv.empresa}")
        cuerpo = quote(
            "Estimados,\n\nAdjunto mi CV para postular a esta convocatoria publicada en "
            "CONECTA UNSA.\n\nSaludos cordiales."
        )
        destino = f"mailto:{destino}?subject={asunto}&body={cuerpo}"
    return RedirectExterno(destino)


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
