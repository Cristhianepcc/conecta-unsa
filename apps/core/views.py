from django.shortcuts import render

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
    """Panel del administrativo (placeholder; la feature 12 lo construye)."""
    return render(request, "core/panel_admin.html")
