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


def registrar_consentimiento(perfil: Perfil) -> None:
    """Marca el consentimiento informado de datos (Ley 29733 / NFR-PRIV-1)."""
    perfil.consentimiento_datos = True
    perfil.consentimiento_en = timezone.now()
    perfil.save(update_fields=["consentimiento_datos", "consentimiento_en"])
