"""Perfiles de usuario (features 02-autenticacion y 07-perfil-credencial).

- Perfil: rol y consentimiento (02). El rol lo decide la identidad, nunca la
  elección del usuario (auth-roles.md §2, NFR-SEC-4).
- PerfilTalento + Credencial: carrera, estado académico, credenciales de doble
  origen, preferencias y credencial pública opt-in (07; perfil-preferencias.md).
"""

from django.conf import settings
from django.db import models

from apps.core import constants
from apps.taxonomia.models import Carrera

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
    # Consentimiento específico para el matching inteligente (Eje 5 · Ley 29733).
    consentimiento_matching = models.BooleanField("consentimiento para matching", default=False)
    consentimiento_matching_en = models.DateTimeField(
        "consentimiento de matching otorgado", null=True, blank=True
    )
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


# --- 07 Perfil de talento y credenciales -----------------------------------
FRECUENCIA_SEMANAL = "semanal"
FRECUENCIAS = [
    (FRECUENCIA_SEMANAL, "Semanal"),
    ("diaria", "Diaria"),
    ("quincenal", "Quincenal"),
    ("ninguna", "No recibir"),
]

FUENTE_VERIFICADO = "verificado"
FUENTE_AUTODECLARADO = "autodeclarado"
FUENTES_CREDENCIAL = [
    (FUENTE_VERIFICADO, "Verificado (sync institucional)"),
    (FUENTE_AUTODECLARADO, "Autodeclarado"),
]

CREDENCIAL_TIPOS = [
    ("idioma", "Idioma"),
    ("taller", "Taller / Curso"),
    ("beca", "Beca"),
    ("olimpiada", "Olimpiada"),
    ("voluntariado", "Voluntariado"),
    ("intercambio", "Intercambio"),
    ("representacion", "Representación estudiantil"),
    ("evento", "Evento / Congreso"),
    ("incubadora_jaku", "Incubadora Jaku"),
    ("practica_convalidada", "Práctica convalidada"),
    ("articulo", "Artículo científico"),
    ("tesis", "Tesis"),
]


class PerfilTalento(models.Model):
    """Perfil de talento del egresado: identidad académica + preferencias + credencial pública.

    TODO producción: `carrera` y `estado_academico` llegarían por sync institucional
    autorizado y serían **solo lectura** (perfil-preferencias.md §1). En demo son autodeclarados.
    """

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_talento",
        verbose_name="usuario",
    )
    carrera = models.ForeignKey(
        Carrera, on_delete=models.PROTECT, null=True, blank=True,
        related_name="egresados", verbose_name="carrera",
    )
    estado_academico = models.CharField(
        "estado académico", max_length=20,
        choices=constants.ESTADOS_ACADEMICOS, blank=True,
    )

    # Interoperabilidad (Eje 2): identidad validada contra el padrón académico UNSA.
    # `dni` es dato personal (Ley 29733): NUNCA se expone en la credencial pública.
    identidad_verificada = models.BooleanField(
        "identidad verificada (padrón UNSA)", default=False
    )
    dni = models.CharField("DNI", max_length=8, blank=True, null=True)

    # Preferencias (afinan el feed; todo funciona sin configurarlas)
    carreras_extra = models.ManyToManyField(
        Carrera, blank=True, related_name="interesados", verbose_name="carreras extra de interés",
    )
    categorias_silenciadas = models.JSONField("categorías silenciadas", default=list, blank=True)
    tipos_preferidos = models.JSONField("tipos preferidos", default=list, blank=True)
    frecuencia = models.CharField(
        "frecuencia de notificación", max_length=20,
        choices=FRECUENCIAS, default=FRECUENCIA_SEMANAL,
    )

    # Credencial pública (opt-in, apagada por defecto — Ley 29733)
    cred_activa = models.BooleanField("credencial pública activa", default=False)
    cred_slug = models.SlugField("slug público", max_length=50, unique=True, null=True, blank=True)

    actualizado_en = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "perfil de talento"
        verbose_name_plural = "perfiles de talento"

    def __str__(self):
        return f"Talento de {self.usuario}"

    @property
    def completo(self) -> bool:
        return bool(self.carrera_id and self.estado_academico)


class Credencial(models.Model):
    """Logro del perfil con fuente (verificado/autodeclarado). matching.md Layer 3."""

    perfil = models.ForeignKey(
        PerfilTalento, on_delete=models.CASCADE, related_name="credenciales", verbose_name="perfil"
    )
    tipo = models.CharField("tipo", max_length=30, choices=CREDENCIAL_TIPOS)
    detalle = models.CharField("detalle (nombre / nivel / fecha)", max_length=255, blank=True)
    fuente = models.CharField(
        "fuente", max_length=20, choices=FUENTES_CREDENCIAL, default=FUENTE_AUTODECLARADO
    )
    visible_para_empresas = models.BooleanField("visible para empresas", default=False)
    creada_en = models.DateTimeField("creada", auto_now_add=True)

    class Meta:
        verbose_name = "credencial"
        verbose_name_plural = "credenciales"
        ordering = ["-creada_en"]

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.detalle}"

    @property
    def verificada(self) -> bool:
        return self.fuente == FUENTE_VERIFICADO

    @property
    def editable(self) -> bool:
        """Solo lo autodeclarado es editable por el egresado (CA-3 / NFR-PRIV-4)."""
        return self.fuente == FUENTE_AUTODECLARADO
