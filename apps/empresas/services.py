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
    """Métricas propias calculadas de datos reales (CA-5)."""
    from django.db.models import Q
    from django.utils import timezone

    from apps.convocatorias.models import (
        ESTADO_PUBLICADA,
        INTERACCION_VISTA,
        InteraccionConvocatoria,
    )
    from apps.matching.services import alcance

    hoy = timezone.localdate()
    convs = empresa.convocatorias.all()
    activas = convs.filter(estado=ESTADO_PUBLICADA).filter(
        Q(fecha_limite__gte=hoy) | Q(fecha_limite__isnull=True)
    )
    vistas = InteraccionConvocatoria.objects.filter(
        convocatoria__empresa=empresa, tipo=INTERACCION_VISTA
    ).count()
    return {
        "activas": activas.count(),
        "publicadas": convs.filter(estado=ESTADO_PUBLICADA).count(),
        "total": convs.count(),
        "alcance": sum(alcance(c) for c in activas),
        "vistas": vistas,
    }
