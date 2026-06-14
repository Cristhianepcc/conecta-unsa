from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.usuarios.decorators import admin_required

from .services import (
    categorias_profesionales,
    convocatorias_destacadas,
    metricas_landing,
    resumen_semanal_landing,
)


def home(request):
    """Landing pública institucional con métricas honestas (feature 09)."""
    return render(
        request,
        "core/home.html",
        {
            "metricas": metricas_landing(),
            "categorias": categorias_profesionales(),
            "destacadas": convocatorias_destacadas(),
            "resumen": resumen_semanal_landing(),
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
    from django.db.models import Avg, Q

    from apps.convocatorias import flujo
    from apps.convocatorias.models import (
        ESTADO_OBSERVADA,
        ESTADO_PENDIENTE,
        ESTADO_PUBLICADA,
        Convocatoria,
    )

    from django.utils import timezone

    q = request.GET.get("q", "").strip()
    filtro = request.GET.get("filtro") or "todas"
    orden = request.GET.get("orden") or "antiguedad"

    por_revisar = (
        Convocatoria.objects.filter(estado__in=[ESTADO_PENDIENTE, ESTADO_OBSERVADA])
        .select_related("empresa")
        .order_by("creada_en")  # FIFO: lo más antiguo (más urgente) primero
    )
    if q:
        por_revisar = por_revisar.filter(
            Q(titulo__icontains=q)
            | Q(empresa__razon_social__icontains=q)
            | Q(empresa__nombre_comercial__icontains=q)
        )

    ahora = timezone.now()
    bandeja, con_duplicado = [], 0
    for conv in por_revisar:
        alertas = flujo.calcular_alertas(conv)
        duplicados = flujo.detectar_duplicado(conv)
        if duplicados:
            con_duplicado += 1
        riesgo = "alto" if duplicados else ("medio" if alertas else "ok")
        bandeja.append(
            {
                "conv": conv,
                "alertas": alertas,
                "duplicados": duplicados,
                "riesgo": riesgo,
                "dias": (ahora - conv.creada_en).days,
            }
        )

    # Conteos para los chips de filtro (sobre el resultado de búsqueda, sin filtrar)
    conteos = {
        "todas": len(bandeja),
        "pendiente": sum(1 for it in bandeja if it["conv"].estado == ESTADO_PENDIENTE),
        "observada": sum(1 for it in bandeja if it["conv"].estado == ESTADO_OBSERVADA),
        "duplicado": sum(1 for it in bandeja if it["duplicados"]),
        "limpias": sum(1 for it in bandeja if not it["alertas"]),
    }

    predicados = {
        "pendiente": lambda it: it["conv"].estado == ESTADO_PENDIENTE,
        "observada": lambda it: it["conv"].estado == ESTADO_OBSERVADA,
        "duplicado": lambda it: bool(it["duplicados"]),
        "limpias": lambda it: not it["alertas"],
    }
    if filtro in predicados:
        bandeja = [it for it in bandeja if predicados[filtro](it)]

    if orden == "riesgo":
        rango = {"alto": 2, "medio": 1, "ok": 0}
        bandeja.sort(key=lambda it: (-rango[it["riesgo"]], it["conv"].creada_en))

    publicadas = Convocatoria.objects.filter(estado=ESTADO_PUBLICADA)
    metricas = {
        "recibidas": Convocatoria.objects.exclude(estado="borrador").count(),
        "pendientes": Convocatoria.objects.filter(estado=ESTADO_PENDIENTE).count(),
        "validadas": publicadas.count(),
        "duplicados": con_duplicado,
        "indice_transparencia": round(
            publicadas.aggregate(p=Avg("transparencia_pct"))["p"] or 0
        ),
    }
    return render(
        request,
        "core/panel_admin.html",
        {
            "bandeja": bandeja,
            "metricas": metricas,
            "conteos": conteos,
            "filtro": filtro,
            "q": q,
            "orden": orden,
        },
    )


@admin_required
@transaction.atomic
def aprobar_lote(request):
    """Aprueba en lote las convocatorias seleccionadas (solo las sin alertas).

    Se ejecuta como una transacción: el lote se procesa de forma consistente y los
    fallos por ítem (alertas o transición inválida) no rompen el resto.
    """
    if request.method != "POST":
        return redirect("core:panel_admin")

    from apps.convocatorias import flujo
    from apps.convocatorias.models import (
        ESTADO_OBSERVADA,
        ESTADO_PENDIENTE,
        Convocatoria,
    )

    ids = request.POST.getlist("ids")
    convs = Convocatoria.objects.filter(
        id__in=ids, estado__in=[ESTADO_PENDIENTE, ESTADO_OBSERVADA]
    )
    aprobadas = omitidas = 0
    for conv in convs:
        if flujo.calcular_alertas(conv):  # seguridad: nunca aprobar con alertas en lote
            omitidas += 1
            continue
        try:
            flujo.aprobar(conv)
            aprobadas += 1
        except flujo.TransicionInvalida:
            omitidas += 1

    if aprobadas and omitidas:
        messages.success(
            request,
            f"Se publicaron {aprobadas} convocatoria(s); {omitidas} omitida(s) por alertas.",
        )
    elif aprobadas:
        messages.success(request, f"Se publicaron {aprobadas} convocatoria(s).")
    else:
        messages.info(request, "No se aprobó ninguna convocatoria (todas tenían alertas).")
    return redirect(_destino_bandeja(request))


def _destino_bandeja(request):
    """URL de retorno a la bandeja preservando filtro/búsqueda (`next` seguro)."""
    from django.urls import reverse
    from django.utils.http import url_has_allowed_host_and_scheme

    nxt = request.POST.get("next") or request.GET.get("next")
    if nxt and url_has_allowed_host_and_scheme(
        nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return nxt
    return reverse("core:panel_admin")


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
        return redirect(_destino_bandeja(request))

    from apps.convocatorias.services import faltantes_nivel_1

    etiquetas = {
        f.name: f.verbose_name
        for f in Convocatoria._meta.get_fields()
        if hasattr(f, "verbose_name")
    }
    faltantes = [etiquetas.get(c, c) for c in faltantes_nivel_1(conv)]

    return render(
        request,
        "core/revisar.html",
        {
            "conv": conv,
            "alertas": flujo.calcular_alertas(conv),
            "duplicados": flujo.detectar_duplicado(conv),
            "faltantes": faltantes,
        },
    )
