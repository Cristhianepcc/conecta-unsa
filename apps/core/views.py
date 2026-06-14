from django.shortcuts import render


def home(request):
    """Página de inicio (placeholder de fundación; la feature 09-landing la reemplaza)."""
    return render(request, "core/home.html")
