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
