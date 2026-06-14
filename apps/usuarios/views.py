"""Vistas de autenticación: 2 puertas (Google / empresa), ruteo y consentimiento."""

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .decorators import egresado_required
from .forms import ConsentimientoForm
from .services import asegurar_perfil, registrar_consentimiento, resolver_rol_y_destino


def login_view(request):
    """Pantalla de login con las 2 puertas (login.png)."""
    if request.user.is_authenticated:
        return redirect("usuarios:post_login")
    return render(request, "usuarios/login.html", {"form_empresa": AuthenticationForm()})


@require_http_methods(["POST"])
def login_empresa(request):
    """Puerta 'Soy empresa': autenticación por usuario/contraseña (auth-roles.md §2)."""
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        return redirect("usuarios:post_login")
    messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "usuarios/login.html", {"form_empresa": form})


@login_required
def post_login(request):
    """Destino tras autenticar: enruta según rol (identidad, no pestaña)."""
    return redirect(resolver_rol_y_destino(request.user))


def logout_view(request):
    auth_logout(request)
    messages.info(request, "Cerraste sesión correctamente.")
    return redirect("core:home")


@login_required
def completar_perfil(request):
    """Primer ingreso del egresado: consentimiento de datos (CA-6).

    La feature 07 amplía esta página con carrera y estado académico.
    """
    perfil = asegurar_perfil(request.user)
    if request.method == "POST":
        form = ConsentimientoForm(request.POST)
        if form.is_valid():
            registrar_consentimiento(perfil)
            perfil.perfil_completo = True
            perfil.save(update_fields=["perfil_completo"])
            messages.success(request, "¡Perfil activado! Bienvenido a CONECTA UNSA.")
            return redirect("usuarios:dashboard")
    else:
        form = ConsentimientoForm()
    return render(request, "usuarios/completar_perfil.html", {"form": form})


@egresado_required
def dashboard(request):
    """Dashboard del egresado (placeholder; la feature 10 lo construye)."""
    return render(request, "usuarios/dashboard.html")
