"""Lógica de empresas: registro, activación y guard de publicación."""

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.usuarios.models import ROL_RECLUTADOR
from apps.usuarios.services import asegurar_perfil

from .models import ESTADO_ACTIVA, ESTADO_RECHAZADA, Empresa, Reclutador

User = get_user_model()


@transaction.atomic
def registrar_empresa(*, empresa: Empresa, reclutador: Reclutador, username: str,
                      password: str) -> Empresa:
    """Crea la cuenta del reclutador (rol=reclutador), la empresa (pendiente) y el vínculo.

    `empresa` y `reclutador` son instancias sin guardar (de los ModelForm).
    """
    user = User.objects.create_user(
        username=username, email=reclutador.email or "", password=password
    )
    perfil = asegurar_perfil(user)
    perfil.rol = ROL_RECLUTADOR
    perfil.save(update_fields=["rol"])

    empresa.save()  # estado por defecto = pendiente (CA-1)

    reclutador.usuario = user
    reclutador.empresa = empresa
    reclutador.save()
    return empresa


def empresa_puede_publicar(empresa: Empresa) -> bool:
    """Guard reutilizable: solo una empresa activa publica convocatorias (CA-2)."""
    return empresa is not None and empresa.estado == ESTADO_ACTIVA


def activar_empresa(empresa: Empresa) -> None:
    empresa.estado = ESTADO_ACTIVA
    empresa.save(update_fields=["estado"])


def rechazar_empresa(empresa: Empresa) -> None:
    empresa.estado = ESTADO_RECHAZADA
    empresa.save(update_fields=["estado"])


def empresa_de(usuario) -> Empresa | None:
    """Empresa vinculada al reclutador autenticado (o None)."""
    reclutador = getattr(usuario, "reclutador", None)
    return reclutador.empresa if reclutador else None


def metricas_empresa(empresa: Empresa) -> dict:
    """Métricas propias calculadas de datos reales (CA-5).

    `vistas` y `guardadas` son dicts {total, delta} donde `delta` es la variación %
    de los últimos 7 días frente a los 7 anteriores (None si no hay base de comparación).
    """
    from datetime import timedelta

    from django.db.models import Q
    from django.utils import timezone

    from apps.convocatorias.models import (
        ESTADO_PUBLICADA,
        INTERACCION_GUARDADA,
        INTERACCION_VISTA,
        InteraccionConvocatoria,
    )
    from apps.matching.services import alcance

    hoy = timezone.localdate()
    sem_ini = hoy - timedelta(days=7)
    sem_prev = hoy - timedelta(days=14)
    convs = empresa.convocatorias.all()
    activas = convs.filter(estado=ESTADO_PUBLICADA).filter(
        Q(fecha_limite__gte=hoy) | Q(fecha_limite__isnull=True)
    )
    inter = InteraccionConvocatoria.objects.filter(convocatoria__empresa=empresa)

    def _con_tendencia(tipo: str) -> dict:
        qs = inter.filter(tipo=tipo)
        ult = qs.filter(creado_en__date__gte=sem_ini).count()
        prev = qs.filter(
            creado_en__date__gte=sem_prev, creado_en__date__lt=sem_ini
        ).count()
        delta = round((ult - prev) / prev * 100) if prev else None
        return {"total": qs.count(), "delta": delta}

    return {
        "activas": activas.count(),
        "publicadas": convs.filter(estado=ESTADO_PUBLICADA).count(),
        "total": convs.count(),
        "alcance": sum(alcance(c) for c in activas),
        "vistas": _con_tendencia(INTERACCION_VISTA),
        "guardadas": _con_tendencia(INTERACCION_GUARDADA),
    }


def completitud_empresa(empresa: Empresa) -> dict:
    """Checklist de completitud del perfil público de la empresa.

    Devuelve {pct, items: [{label, ok}]} para el panel "Estado de tu empresa".
    """
    items = [
        {"label": "Descripción de la empresa", "ok": bool(empresa.descripcion.strip())},
        {"label": "Logo", "ok": bool(empresa.logo_img or empresa.logo_url.strip())},
        {"label": "Sitio web o LinkedIn", "ok": bool(empresa.web.strip() or empresa.linkedin.strip())},
        {"label": "Teléfono de contacto", "ok": bool(empresa.telefono.strip())},
        {"label": "Dirección", "ok": bool(empresa.direccion.strip())},
    ]
    completos = sum(1 for i in items if i["ok"])
    pct = round(completos / len(items) * 100) if items else 0
    return {"pct": pct, "items": items, "completos": completos, "total": len(items)}
