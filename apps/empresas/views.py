from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.convocatorias import flujo
from apps.convocatorias.forms import ConvocatoriaForm
from apps.convocatorias.models import (
    CREADA_POR_EMPRESA,
    ESTADO_OBSERVADA,
    Convocatoria,
)
from apps.convocatorias.services import faltantes_nivel_1, validar_legal
from apps.usuarios.decorators import empresa_required

from .forms import EmpresaForm, ReclutadorForm
from .services import empresa_de, metricas_empresa, registrar_empresa


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
    if empresa.puede_publicar:
        contexto["metricas"] = metricas_empresa(empresa)
        contexto["convocatorias"] = empresa.convocatorias.all()
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
    return render(request, "empresas/publicar.html", {"form": form, "empresa": empresa})


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
        {"form": form, "conv": conv, "observada": conv.estado == ESTADO_OBSERVADA},
    )


def registro(request):
    """Auto-registro de empresa: bloque A (empresa) + bloque B (reclutador). CA-1/CA-7 (feature 03)."""
    if request.method == "POST":
        empresa_form = EmpresaForm(request.POST)
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
