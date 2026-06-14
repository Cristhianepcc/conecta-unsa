from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.convocatorias import flujo
from apps.convocatorias.forms import ConvocatoriaForm
from apps.convocatorias.models import (
    CREADA_POR_EMPRESA,
    ESTADO_OBSERVADA,
    Convocatoria,
)
from apps.convocatorias.services import (
    desglose_transparencia,
    faltantes_nivel_1,
    puntos_por_criterio,
    validar_legal,
)
from apps.usuarios.decorators import empresa_required

from .forms import EditarEmpresaForm, EmpresaForm, ReclutadorForm
from .services import (
    completitud_empresa,
    empresa_de,
    metricas_empresa,
    registrar_empresa,
)


@empresa_required
def dashboard(request):
    """Inicio de la empresa: métricas propias + mis convocatorias (CA-1/CA-5).

    Si la empresa no está verificada, se muestra un dashboard limitado (CA-3).
    """
    empresa = empresa_de(request.user)
    contexto = {"empresa": empresa}
    if empresa is None:
        return render(request, "empresas/dashboard.html", contexto)

    contexto["puede_publicar"] = empresa.puede_publicar
    contexto["completitud"] = completitud_empresa(empresa)
    if empresa.puede_publicar:
        from django.utils import timezone

        hoy = timezone.localdate()
        contexto["metricas"] = metricas_empresa(empresa)
        convs = list(empresa.convocatorias.all())
        conteos = {"todas": len(convs)}
        suma_pct = 0
        agg = {}
        for c in convs:
            desg = desglose_transparencia(c)
            # Coaching de transparencia: qué falta y cuánto sumaría (CA-6).
            c.faltan_transp = [i for i in desg if not i["presente"]]
            # Urgencia de la fecha límite (días restantes; None si no tiene).
            c.dias_restantes = (c.fecha_limite - hoy).days if c.fecha_limite else None
            conteos[c.estado] = conteos.get(c.estado, 0) + 1
            suma_pct += c.transparencia_pct
            # Agregado real de transparencia para el panel lateral.
            for item in desg:
                a = agg.setdefault(
                    item["criterio"],
                    {"etiqueta": item["etiqueta"], "puntos": item["puntos"], "cumplen": 0},
                )
                if item["presente"]:
                    a["cumplen"] += 1
        contexto["convocatorias"] = convs
        contexto["conteos"] = conteos
        # Banda de atención: lo accionable primero (observadas / por vencer ≤7 días).
        observadas = [c for c in convs if c.estado == ESTADO_OBSERVADA]
        por_vencer = [
            c
            for c in convs
            if c.estado == "publicada"
            and c.dias_restantes is not None
            and 0 <= c.dias_restantes <= 7
        ]
        contexto["atencion"] = {
            "observadas": len(observadas),
            "obs_unica": observadas[0] if len(observadas) == 1 else None,
            "por_vencer": len(por_vencer),
        }
        if convs:
            criterios = sorted(
                agg.values(), key=lambda a: (a["cumplen"] / len(convs), -a["puntos"])
            )
            for a in criterios:
                a["total"] = len(convs)
                a["falta"] = len(convs) - a["cumplen"]
            contexto["transparencia_resumen"] = {
                "promedio": round(suma_pct / len(convs)),
                "total": len(convs),
                "criterios": criterios[:4],
            }
    return render(request, "empresas/dashboard.html", contexto)


def _guardar_y_enviar(request, conv):
    """Valida Nivel 1 + legal; si ok aplica el semáforo (06). Devuelve lista de errores."""
    faltan = faltantes_nivel_1(conv)
    errores = []
    if faltan:
        errores.append("Faltan campos fundamentales o la declaración de no discriminación.")
    errores.extend(validar_legal(conv))
    if errores:
        return errores
    destino = flujo.procesar_envio(conv)
    if destino == "auto":
        messages.success(request, "¡Convocatoria publicada automáticamente! (empresa verificada, 🟢)")
    else:
        messages.success(request, "Convocatoria enviada a revisión.")
    return []


@empresa_required
def publicar(request):
    """Formulario de publicar (3 bloques, dinámico por tipo). Requiere empresa verificada (CA-2/CA-3)."""
    empresa = empresa_de(request.user)
    if empresa is None or not empresa.puede_publicar:
        messages.error(request, "Tu cuenta aún está en verificación: todavía no puedes publicar.")
        return redirect("empresas:dashboard")

    if request.method == "POST":
        form = ConvocatoriaForm(request.POST)
        if form.is_valid():
            conv = form.save(commit=False)
            conv.empresa = empresa
            conv.creada_por = CREADA_POR_EMPRESA
            conv.save()
            form.save_m2m()
            errores = _guardar_y_enviar(request, conv)
            if not errores:
                return redirect("empresas:dashboard")
            for e in errores:
                messages.error(request, e)
    else:
        form = ConvocatoriaForm()
    return render(
        request,
        "empresas/publicar.html",
        {"form": form, "empresa": empresa, "puntos_transp": puntos_por_criterio()},
    )


@empresa_required
def editar_convocatoria(request, pk):
    """Editar / corregir una convocatoria (incluye observadas con su comentario, CA-4)."""
    empresa = empresa_de(request.user)
    conv = get_object_or_404(Convocatoria, pk=pk, empresa=empresa)

    if request.method == "POST":
        form = ConvocatoriaForm(request.POST, instance=conv)
        if form.is_valid():
            conv = form.save()
            errores = _guardar_y_enviar(request, conv)
            if not errores:
                messages.success(request, "Convocatoria actualizada y reenviada.")
                return redirect("empresas:dashboard")
            for e in errores:
                messages.error(request, e)
    else:
        form = ConvocatoriaForm(instance=conv)
    return render(
        request, "empresas/editar.html",
        {
            "form": form,
            "conv": conv,
            "observada": conv.estado == ESTADO_OBSERVADA,
            "puntos_transp": puntos_por_criterio(),
        },
    )


@empresa_required
def editar_perfil(request):
    """Edición del perfil público de la empresa (cierra el ciclo de la completitud)."""
    empresa = empresa_de(request.user)
    if empresa is None:
        return redirect("empresas:dashboard")

    if request.method == "POST":
        form = EditarEmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil de empresa actualizado.")
            return redirect("empresas:dashboard")
    else:
        form = EditarEmpresaForm(instance=empresa)
    return render(
        request,
        "empresas/editar_perfil.html",
        {"form": form, "empresa": empresa, "completitud": completitud_empresa(empresa)},
    )


def registro(request):
    """Auto-registro de empresa: bloque A (empresa) + bloque B (reclutador). CA-1/CA-7 (feature 03)."""
    if request.method == "POST":
        empresa_form = EmpresaForm(request.POST, request.FILES)
        reclutador_form = ReclutadorForm(request.POST)
        if empresa_form.is_valid() and reclutador_form.is_valid():
            registrar_empresa(
                empresa=empresa_form.save(commit=False),
                reclutador=reclutador_form.save(commit=False),
                username=reclutador_form.cleaned_data["username"],
                password=reclutador_form.cleaned_data["password1"],
            )
            # Estado de éxito contextual (Post/Redirect/Get): evita el banner global
            # desconectado del flujo y previene reenvío al refrescar.
            return redirect("empresas:registro_exito")
    else:
        empresa_form = EmpresaForm()
        reclutador_form = ReclutadorForm()

    return render(
        request,
        "empresas/registro.html",
        {"empresa_form": empresa_form, "reclutador_form": reclutador_form},
    )


def registro_exito(request):
    """Pantalla de confirmación posterior al registro de empresa (feedback en contexto)."""
    return render(request, "empresas/registro_exito.html")
