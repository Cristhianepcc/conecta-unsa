from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.decorators import admin_required

from .services import categorias_con_conteo, metricas_landing


def home(request):
    """Landing pública institucional con métricas honestas (feature 09)."""
    return render(
        request,
        "core/home.html",
        {
            "metricas": metricas_landing(),
            "categorias": categorias_con_conteo(),
        },
    )


def como_funciona(request):
    return render(request, "core/como_funciona.html")


def privacidad(request):
    return render(request, "core/privacidad.html")


def terminos(request):
    return render(request, "core/terminos.html")


@admin_required
def panel_admin(request):
    """Bandeja priorizada + métricas para la Bolsa de Trabajo (feature 12)."""
    from django.db.models import Avg

    from apps.convocatorias import flujo
    from apps.convocatorias.models import (
        ESTADO_OBSERVADA,
        ESTADO_PENDIENTE,
        ESTADO_PUBLICADA,
        Convocatoria,
    )

    por_revisar = (
        Convocatoria.objects.filter(estado__in=[ESTADO_PENDIENTE, ESTADO_OBSERVADA])
        .select_related("empresa")
    )
    bandeja, con_duplicado = [], 0
    for conv in por_revisar:
        alertas = flujo.calcular_alertas(conv)
        duplicados = flujo.detectar_duplicado(conv)
        if duplicados:
            con_duplicado += 1
        bandeja.append({"conv": conv, "alertas": alertas, "duplicados": duplicados})

    publicadas = Convocatoria.objects.filter(estado=ESTADO_PUBLICADA)
    metricas = {
        "recibidas": Convocatoria.objects.exclude(estado="borrador").count(),
        "pendientes": por_revisar.filter(estado=ESTADO_PENDIENTE).count(),
        "validadas": publicadas.count(),
        "duplicados": con_duplicado,
        "indice_transparencia": round(
            publicadas.aggregate(p=Avg("transparencia_pct"))["p"] or 0
        ),
    }
    return render(
        request, "core/panel_admin.html", {"bandeja": bandeja, "metricas": metricas}
    )


@admin_required
def revisar_convocatoria(request, pk):
    """Revisar una convocatoria: aprobar / observar (comentario) / rechazar (CA-2)."""
    from apps.convocatorias import flujo
    from apps.convocatorias.models import Convocatoria

    conv = get_object_or_404(Convocatoria, pk=pk)
    if request.method == "POST":
        accion = request.POST.get("accion")
        comentario = request.POST.get("comentario", "").strip()
        try:
            if accion == "aprobar":
                flujo.aprobar(conv)
                messages.success(request, "Convocatoria publicada.")
            elif accion == "observar":
                if not comentario:
                    messages.error(request, "Debes escribir un comentario para observar.")
                    return redirect("core:revisar_convocatoria", pk=pk)
                flujo.observar(conv, comentario)
                messages.success(request, "Convocatoria observada y notificada a la empresa.")
            elif accion == "rechazar":
                flujo.rechazar(conv, comentario)
                messages.success(request, "Convocatoria rechazada.")
            else:
                messages.error(request, "Acción no válida.")
                return redirect("core:revisar_convocatoria", pk=pk)
        except flujo.TransicionInvalida as e:
            messages.error(request, str(e))
            return redirect("core:revisar_convocatoria", pk=pk)
        return redirect("core:panel_admin")

    return render(
        request,
        "core/revisar.html",
        {
            "conv": conv,
            "alertas": flujo.calcular_alertas(conv),
            "duplicados": flujo.detectar_duplicado(conv),
        },
    )
