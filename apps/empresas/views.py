from django.contrib import messages
from django.shortcuts import redirect, render

from apps.usuarios.decorators import empresa_required

from .forms import EmpresaForm, ReclutadorForm
from .services import registrar_empresa


@empresa_required
def dashboard(request):
    """Dashboard de la empresa (placeholder; la feature 11 lo construye)."""
    return render(request, "empresas/dashboard.html")


def registro(request):
    """Auto-registro de empresa: bloque A (empresa) + bloque B (reclutador). CA-1/CA-7."""
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
            messages.success(
                request,
                "Registro enviado. Tu cuenta será verificada por la universidad antes de publicar.",
            )
            return redirect("usuarios:login")
    else:
        empresa_form = EmpresaForm()
        reclutador_form = ReclutadorForm()

    return render(
        request,
        "empresas/registro.html",
        {"empresa_form": empresa_form, "reclutador_form": reclutador_form},
    )
