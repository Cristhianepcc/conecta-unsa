"""Perfil de usuario: rol y consentimiento de datos (feature 02-autenticacion).

El rol lo decide la identidad (allowlist / tipo de login), nunca la elección del
usuario (auth-roles.md §2, NFR-SEC-4). Los campos académicos (carrera, estado) y
PerfilTalento los agrega la feature 07-perfil-credencial sobre esta misma app.
"""

from django.conf import settings
from django.db import models

ROL_EGRESADO = "egresado"
ROL_ADMIN = "admin"
ROL_RECLUTADOR = "reclutador"

ROLES = [
    (ROL_EGRESADO, "Estudiante / Egresado"),
    (ROL_ADMIN, "Administrativo"),
    (ROL_RECLUTADOR, "Reclutador (empresa)"),
]


class Perfil(models.Model):
    """Datos transversales de cuenta (1-1 con el User de Django)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name="usuario",
    )
    rol = models.CharField("rol", max_length=20, choices=ROLES, default=ROL_EGRESADO)
    consentimiento_datos = models.BooleanField("consentimiento de datos", default=False)
    consentimiento_en = models.DateTimeField("consentimiento otorgado", null=True, blank=True)
    perfil_completo = models.BooleanField("perfil completo", default=False)

    creado_en = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"{self.user} ({self.rol})"

    @property
    def es_admin(self):
        return self.rol == ROL_ADMIN

    @property
    def es_reclutador(self):
        return self.rol == ROL_RECLUTADOR

    @property
    def es_egresado(self):
        return self.rol == ROL_EGRESADO
