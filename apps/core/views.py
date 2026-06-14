from django.shortcuts import render

from apps.usuarios.decorators import admin_required


def home(request):
    """Página de inicio (placeholder de fundación; la feature 09-landing la reemplaza)."""
    return render(request, "core/home.html")


@admin_required
def panel_admin(request):
    """Panel del administrativo (placeholder; la feature 12 lo construye)."""
    return render(request, "core/panel_admin.html")
