from django.shortcuts import render

from apps.usuarios.decorators import empresa_required


@empresa_required
def dashboard(request):
    """Dashboard de la empresa (placeholder; la feature 11 lo construye)."""
    return render(request, "empresas/dashboard.html")


def registro(request):
    """Registro de empresa (placeholder; la feature 03 lo construye)."""
    return render(request, "empresas/registro.html")
