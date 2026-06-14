"""Vistas de autenticación (02) y perfil/credencial (07)."""

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .decorators import egresado_required
from .forms import (
    CompletarPerfilForm,
    CredencialForm,
    PreferenciasForm,
)
from .models import FUENTE_AUTODECLARADO, PerfilTalento
from .services import (
    activar_credencial_publica,
    asegurar_perfil,
    asegurar_perfil_talento,
    registrar_consentimiento,
    resolver_rol_y_destino,
    revocar_credencial_publica,
)


# --- 02 Autenticación -------------------------------------------------------
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
    """Primer ingreso del egresado: carrera + estado académico + consentimiento (CA-1 / CA-6)."""
    perfil = asegurar_perfil(request.user)
    talento = asegurar_perfil_talento(request.user)
    if request.method == "POST":
        form = CompletarPerfilForm(request.POST)
        if form.is_valid():
            talento.carrera = form.cleaned_data["carrera"]
            talento.estado_academico = form.cleaned_data["estado_academico"]
            talento.save(update_fields=["carrera", "estado_academico"])
            registrar_consentimiento(perfil)
            perfil.perfil_completo = True
            perfil.save(update_fields=["perfil_completo"])
            messages.success(request, "¡Perfil activado! Bienvenido a CONECTA UNSA.")
            return redirect("usuarios:dashboard")
    else:
        form = CompletarPerfilForm(
            initial={"carrera": talento.carrera_id, "estado_academico": talento.estado_academico}
        )
    return render(request, "usuarios/completar_perfil.html", {"form": form})


@egresado_required
def dashboard(request):
    """Dashboard del egresado: feed pertinente ordenado + resumen + campana (feature 10)."""
    from apps.matching.services import feed as matching_feed

    items = matching_feed(request.user)  # [(conv, puntaje, motivos)]
    talento = asegurar_perfil_talento(request.user)
    return render(
        request,
        "usuarios/dashboard.html",
        {
            "items": items,
            "talento": talento,
            "resumen": [conv for conv, _p, _m in items[:5]],
        },
    )


@egresado_required
def guardadas(request):
    from apps.convocatorias.interacciones import guardadas_de

    return render(
        request, "usuarios/guardadas.html", {"convocatorias": guardadas_de(request.user)}
    )


@egresado_required
def historial(request):
    from apps.convocatorias.interacciones import historial_de

    return render(
        request, "usuarios/historial.html", {"convocatorias": historial_de(request.user)}
    )


# --- 07 Perfil de talento y credenciales ------------------------------------
@egresado_required
def perfil(request):
    """Edita preferencias y administra credenciales autodeclaradas (CA-2/CA-4)."""
    talento = asegurar_perfil_talento(request.user)

    if request.method == "POST" and "guardar_preferencias" in request.POST:
        pref_form = PreferenciasForm(request.POST, instance=talento)
        if pref_form.is_valid():
            pref_form.save()
            messages.success(request, "Preferencias guardadas.")
            return redirect("usuarios:perfil")
    else:
        pref_form = PreferenciasForm(instance=talento)

    cred_form = CredencialForm()
    if request.method == "POST" and "agregar_credencial" in request.POST:
        cred_form = CredencialForm(request.POST)
        if cred_form.is_valid():
            credencial = cred_form.save(commit=False)
            credencial.perfil = talento
            credencial.fuente = FUENTE_AUTODECLARADO  # el egresado solo agrega autodeclaradas
            credencial.save()
            messages.success(request, "Credencial agregada.")
            return redirect("usuarios:perfil")

    return render(
        request,
        "usuarios/perfil.html",
        {
            "talento": talento,
            "pref_form": pref_form,
            "cred_form": cred_form,
            "credenciales": talento.credenciales.all(),
        },
    )


@egresado_required
def eliminar_credencial(request, credencial_id):
    """Elimina una credencial autodeclarada (las verificadas son solo lectura, CA-3)."""
    talento = asegurar_perfil_talento(request.user)
    credencial = get_object_or_404(talento.credenciales, pk=credencial_id)
    if not credencial.editable:
        messages.error(request, "Las credenciales verificadas no se pueden editar ni eliminar.")
    elif request.method == "POST":
        credencial.delete()
        messages.success(request, "Credencial eliminada.")
    return redirect("usuarios:perfil")


@egresado_required
def credencial_config(request):
    """Activa / revoca la credencial pública y controla su visibilidad (CA-5/CA-7)."""
    talento = asegurar_perfil_talento(request.user)
    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "activar":
            slug = activar_credencial_publica(talento)
            messages.success(request, f"Credencial pública activada: /credencial/{slug}")
        elif accion == "revocar":
            revocar_credencial_publica(talento)
            messages.info(request, "Credencial pública revocada.")
        return redirect("usuarios:credencial_config")
    return render(request, "usuarios/credencial_config.html", {"talento": talento})


def credencial_publica(request, slug):
    """Carta de presentación pública: solo lectura, noindex, sin features sociales (CA-6)."""
    talento = get_object_or_404(PerfilTalento, cred_slug=slug, cred_activa=True)
    credenciales = talento.credenciales.filter(visible_para_empresas=True)
    response = render(
        request,
        "usuarios/credencial_publica.html",
        {"talento": talento, "credenciales": credenciales},
    )
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response
