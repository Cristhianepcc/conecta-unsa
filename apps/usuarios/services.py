"""Ruteo de rol post-login (auth-roles.md §2).

Regla de seguridad: el rol lo decide la **identidad**, no la pestaña elegida.
- admin  → SOLO si el correo está en AdminAllowlist (NFR-SEC-4).
- reclutador → usuario con empresa vinculada (Perfil.rol=reclutador, lo fija la feature 03).
- egresado → cualquier otro usuario autenticado por Google.
"""

from django.utils import timezone

from apps.core.models import AdminAllowlist

from .models import ROL_ADMIN, ROL_EGRESADO, ROL_RECLUTADOR, Perfil

# Destino (nombre de URL) por rol.
DESTINO_POR_ROL = {
    ROL_ADMIN: "core:panel_admin",
    ROL_RECLUTADOR: "empresas:dashboard",
    ROL_EGRESADO: "usuarios:dashboard",
}


def asegurar_perfil(user) -> Perfil:
    """Devuelve (creando si hace falta) el Perfil del usuario."""
    perfil, _ = Perfil.objects.get_or_create(user=user)
    return perfil


def _esta_en_allowlist(email: str) -> bool:
    return bool(email) and AdminAllowlist.objects.filter(email__iexact=email).exists()


def resolver_rol(user) -> str:
    """Calcula y persiste el rol del usuario según su identidad."""
    perfil = asegurar_perfil(user)

    # La allowlist es autoritativa para admin (NFR-SEC-4): se reevalúa en cada login,
    # así agregar un correo a la allowlist lo promueve a admin en su próximo ingreso.
    if _esta_en_allowlist(user.email):
        if perfil.rol != ROL_ADMIN:
            perfil.rol = ROL_ADMIN
            perfil.save(update_fields=["rol"])
        return ROL_ADMIN

    # Un reclutador conserva su rol (lo asigna el registro de empresa, feature 03).
    if perfil.rol == ROL_RECLUTADOR:
        return ROL_RECLUTADOR

    if perfil.rol != ROL_EGRESADO:
        perfil.rol = ROL_EGRESADO
        perfil.save(update_fields=["rol"])
    return ROL_EGRESADO


def resolver_rol_y_destino(user) -> str:
    """Devuelve el nombre de URL al que enrutar al usuario tras autenticarse."""
    rol = resolver_rol(user)
    perfil = user.perfil

    # Egresado en su primer ingreso → completar perfil (consentimiento + datos académicos).
    if rol == ROL_EGRESADO and not perfil.perfil_completo:
        return "usuarios:completar_perfil"

    return DESTINO_POR_ROL.get(rol, "usuarios:dashboard")


def registrar_consentimiento(perfil: Perfil, matching: bool = False) -> None:
    """Marca el consentimiento informado de datos (Ley 29733 / NFR-PRIV-1).

    `matching=True` registra además la autorización explícita para el matching
    inteligente (Eje 5), con su propia marca de tiempo para auditoría.
    """
    ahora = timezone.now()
    perfil.consentimiento_datos = True
    perfil.consentimiento_en = ahora
    campos = ["consentimiento_datos", "consentimiento_en"]
    if matching:
        perfil.consentimiento_matching = True
        perfil.consentimiento_matching_en = ahora
        campos += ["consentimiento_matching", "consentimiento_matching_en"]
    perfil.save(update_fields=campos)


# --- 07 Perfil de talento / credencial pública ------------------------------
def asegurar_perfil_talento(user):
    """Devuelve (creando si hace falta) el PerfilTalento del usuario."""
    from .models import PerfilTalento

    perfil_talento, _ = PerfilTalento.objects.get_or_create(usuario=user)
    return perfil_talento


def _slug_unico(base: str) -> str:
    from django.utils.text import slugify

    from .models import PerfilTalento

    raiz = slugify(base) or "credencial"
    slug = raiz
    i = 1
    while PerfilTalento.objects.filter(cred_slug=slug).exists():
        i += 1
        slug = f"{raiz}-{i}"
    return slug


def activar_credencial_publica(perfil_talento) -> str:
    """Activa la credencial pública y genera (si falta) su slug único (CA-5)."""
    if not perfil_talento.cred_slug:
        base = perfil_talento.usuario.get_full_name() or perfil_talento.usuario.username
        perfil_talento.cred_slug = _slug_unico(base)
    perfil_talento.cred_activa = True
    perfil_talento.save(update_fields=["cred_activa", "cred_slug"])
    return perfil_talento.cred_slug


def revocar_credencial_publica(perfil_talento) -> None:
    """Apaga la URL pública; conserva el slug para no reasignarlo (CA-7)."""
    perfil_talento.cred_activa = False
    perfil_talento.save(update_fields=["cred_activa"])


def completitud_perfil(perfil_talento) -> dict:
    """Medidor de completitud del perfil ('mejora progresiva'): % + checklist de pasos."""
    n_cred = perfil_talento.credenciales.count()
    items = [
        {"label": "Define tu carrera", "done": bool(perfil_talento.carrera_id)},
        {"label": "Indica tu estado académico", "done": bool(perfil_talento.estado_academico)},
        {"label": "Agrega tu primera credencial", "done": n_cred >= 1},
        {"label": "Suma 3 o más credenciales", "done": n_cred >= 3},
        {"label": "Elige tus tipos preferidos", "done": bool(perfil_talento.tipos_preferidos)},
        {"label": "Activa tu credencial pública", "done": perfil_talento.cred_activa},
    ]
    total = len(items)
    hechos = sum(1 for it in items if it["done"])
    return {
        "pct": round(hechos / total * 100),
        "hechos": hechos,
        "total": total,
        "items": items,
    }
