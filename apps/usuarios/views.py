"""Vistas de autenticación (02) y perfil/credencial (07)."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
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
    completitud_perfil,
    registrar_consentimiento,
    resolver_rol_y_destino,
    revocar_credencial_publica,
)


# --- 02 Autenticación -------------------------------------------------------
def login_view(request):
    """Pantalla de login con las 2 puertas (login.png)."""
    if request.user.is_authenticated:
        return redirect("usuarios:post_login")
    return render(
        request,
        "usuarios/login.html",
        {"form_empresa": AuthenticationForm(), "demo_mode": settings.DEMO_MODE},
    )


def demo_login(request, rol):
    """Acceso directo a un dashboard para la DEMO (sin Google). Solo con DEMO_MODE=True.

    ⚠️ Inseguro a propósito: existe únicamente para que el jurado vea los flujos de
    egresado y administrativo. En producción real se apaga con DEMO_MODE=False.
    """
    if not settings.DEMO_MODE:
        raise Http404("Disponible solo en modo demo.")

    User = get_user_model()
    if rol == "egresado":
        from apps.taxonomia.models import Carrera

        user, _ = User.objects.get_or_create(
            username="demo_egresado",
            defaults={"email": "demo.egresado@unsa.edu.pe",
                      "first_name": "Demo", "last_name": "Egresado"},
        )
        perfil = asegurar_perfil(user)
        perfil.perfil_completo = True
        perfil.consentimiento_datos = True
        perfil.save()
        talento = asegurar_perfil_talento(user)
        if not talento.carrera_id:
            talento.carrera = (
                Carrera.objects.filter(nombre="Ingeniería Industrial").first()
                or Carrera.objects.first()
            )
            talento.estado_academico = "egresado"
            talento.save()
    elif rol == "admin":
        from apps.core.models import AdminAllowlist
        from .services import resolver_rol

        email = "demo.admin@unsa.edu.pe"
        AdminAllowlist.objects.get_or_create(email=email, defaults={"nota": "Admin demo"})
        user, _ = User.objects.get_or_create(
            username="demo_admin",
            defaults={"email": email, "first_name": "Demo", "last_name": "Admin"},
        )
        resolver_rol(user)  # la allowlist lo promueve a admin
    else:
        raise Http404("Rol de demo no válido.")

    auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("usuarios:post_login")


@require_http_methods(["POST"])
def login_empresa(request):
    """Puerta 'Soy empresa': autenticación por usuario/contraseña (auth-roles.md §2)."""
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        return redirect("usuarios:post_login")
    # Error contextual dentro de la pestaña «Soy empresa», no como banner global.
    return render(
        request,
        "usuarios/login.html",
        {
            "form_empresa": form,
            "puerta_inicial": "empresa",
            "error_empresa": "Usuario o contraseña incorrectos.",
            "demo_mode": settings.DEMO_MODE,
        },
    )


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

    from collections import Counter

    from apps.convocatorias.interacciones import guardadas_de, ids_guardadas
    from apps.core import constants
    from apps.matching.services import compatibilidad

    talento = asegurar_perfil_talento(request.user)
    full = matching_feed(request.user)  # [(conv, puntaje, motivos)] ordenado por afinidad

    # Filtro por tipo + orden (chips estables sobre el conjunto completo).
    labels = dict(constants.TIPOS_CONVOCATORIA)
    conteo = Counter(it[0].tipo for it in full)
    tipos_presentes = [
        {"value": v, "label": labels.get(v, v), "n": n} for v, n in conteo.most_common()
    ]

    tipo = request.GET.get("tipo") or ""
    orden = request.GET.get("orden") or "afinidad"
    seleccion = [it for it in full if it[0].tipo == tipo] if tipo else list(full)
    if orden == "reciente":
        seleccion.sort(key=lambda it: it[0].creada_en, reverse=True)
    elif orden == "transparencia":
        seleccion.sort(key=lambda it: it[0].transparencia_pct, reverse=True)

    # Enriquecer con compatibilidad (% match) + chips de recomendación.
    items = []
    for conv, _puntaje, _motivos in seleccion:
        pct, chips = compatibilidad(request.user, conv)
        items.append({"conv": conv, "match": pct, "chips": chips})

    return render(
        request,
        "usuarios/dashboard.html",
        {
            "items": items,
            "talento": talento,
            "total": len(items),
            "tipo": tipo,
            "orden": orden,
            "tipos_presentes": tipos_presentes,
            "completitud": completitud_perfil(talento),
            "guardadas_ids": ids_guardadas(request.user),
            # "Tu actividad" (sección inferior compacta)
            "n_guardadas": guardadas_de(request.user).count(),
            "resumen_n": len(full),
        },
    )


def _items_con_match(usuario, convocatorias):
    """Construye items {conv, match, chips} para reusar la tarjeta de oportunidad."""
    from apps.matching.services import compatibilidad

    items = []
    for conv in convocatorias:
        pct, chips = compatibilidad(usuario, conv)
        items.append({"conv": conv, "match": pct, "chips": chips})
    return items


@egresado_required
def guardadas(request):
    from apps.convocatorias.interacciones import guardadas_de, ids_guardadas

    return render(
        request,
        "usuarios/guardadas.html",
        {
            "items": _items_con_match(request.user, guardadas_de(request.user)),
            "guardadas_ids": ids_guardadas(request.user),
        },
    )


@egresado_required
def historial(request):
    from apps.convocatorias.interacciones import historial_de, ids_guardadas

    return render(
        request,
        "usuarios/historial.html",
        {
            "items": _items_con_match(request.user, historial_de(request.user)),
            "guardadas_ids": ids_guardadas(request.user),
        },
    )


# --- 07 Perfil de talento y credenciales ------------------------------------
@egresado_required
def perfil(request):
    """Edita preferencias y administra credenciales autodeclaradas (CA-2/CA-4)."""
    from apps.core import constants

    talento = asegurar_perfil_talento(request.user)

    if request.method == "POST" and "guardar_preferencias" in request.POST:
        pref_form = PreferenciasForm(request.POST, instance=talento)
        if pref_form.is_valid():
            obj = pref_form.save(commit=False)
            # Matriz tri-estado de tipos (preferido / normal / silenciado).
            preferidos, silenciados = [], []
            for value, _label in constants.TIPOS_CONVOCATORIA:
                estado = request.POST.get(f"tipo_{value}", "normal")
                if estado == "preferido":
                    preferidos.append(value)
                elif estado == "silenciado":
                    silenciados.append(value)
            obj.tipos_preferidos = preferidos
            obj.categorias_silenciadas = silenciados
            obj.save()
            pref_form.save_m2m()
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

    preferidos = talento.tipos_preferidos or []
    silenciados = talento.categorias_silenciadas or []
    tipos_estado = [
        {
            "value": v,
            "label": label,
            "estado": "preferido" if v in preferidos else ("silenciado" if v in silenciados else "normal"),
        }
        for v, label in constants.TIPOS_CONVOCATORIA
    ]

    return render(
        request,
        "usuarios/perfil.html",
        {
            "talento": talento,
            "pref_form": pref_form,
            "cred_form": cred_form,
            "credenciales": talento.credenciales.all(),
            "completitud": completitud_perfil(talento),
            "tipos_estado": tipos_estado,
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
    return render(
        request,
        "usuarios/credencial_config.html",
        {
            "talento": talento,
            "visibles": talento.credenciales.filter(visible_para_empresas=True),
            "ocultas": talento.credenciales.filter(visible_para_empresas=False).count(),
        },
    )


# Ícono Lucide por tipo de credencial (página pública de credencial).
ICONOS_CREDENCIAL = {
    "idioma": "languages",
    "tesis": "file-text",
    "articulo": "file-text",
    "voluntariado": "heart-handshake",
    "representacion": "users",
    "practica_convalidada": "briefcase",
    "beca": "award",
    "olimpiada": "trophy",
    "intercambio": "globe",
    "incubadora_jaku": "rocket",
    "taller": "graduation-cap",
    "evento": "calendar-days",
}


def credencial_publica(request, slug):
    """Carta de presentación pública verificable: solo lectura, noindex, sin features sociales (CA-6)."""
    import io

    import segno
    from django.urls import reverse
    from django.utils.safestring import mark_safe

    talento = get_object_or_404(PerfilTalento, cred_slug=slug, cred_activa=True)
    credenciales = [
        {"obj": c, "icono": ICONOS_CREDENCIAL.get(c.tipo, "badge-check")}
        for c in talento.credenciales.filter(visible_para_empresas=True)
    ]

    url_abs = request.build_absolute_uri(
        reverse("usuarios:credencial_publica", args=[slug])
    )
    buff = io.BytesIO()
    segno.make(url_abs, error="m").save(
        buff, kind="svg", scale=4, border=0, dark="#0F172A", xmldecl=False
    )
    qr_svg = mark_safe(buff.getvalue().decode())

    response = render(
        request,
        "usuarios/credencial_publica.html",
        {
            "talento": talento,
            "credenciales": credenciales,
            "qr_svg": qr_svg,
            "codigo": slug.upper(),
            "url_publica": url_abs,
            "verificada_en": talento.actualizado_en,
        },
    )
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response
