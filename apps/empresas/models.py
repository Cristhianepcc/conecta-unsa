"""Empresas y reclutadores (feature 03). Referencia: auth-roles.md §4-7.

- Empresa registrada = tiene reclutador vinculado + estado activa → badge «Verificada».
- Empresa referencial = la crea el admin sin reclutador → sin badge (es_referencial).
Archivos (logo/banner) van como URL por el FS efímero de Railway (NFR-PERF-3 / CA-6).
"""

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

ESTADO_PENDIENTE = "pendiente"
ESTADO_ACTIVA = "activa"
ESTADO_RECHAZADA = "rechazada"

ESTADOS_EMPRESA = [
    (ESTADO_PENDIENTE, "Pendiente de activación"),
    (ESTADO_ACTIVA, "Activa"),
    (ESTADO_RECHAZADA, "Rechazada"),
]

TIPOS_EMPRESA = [
    ("sac", "S.A.C."),
    ("sa", "S.A."),
    ("srl", "S.R.L."),
    ("eirl", "E.I.R.L."),
    ("ong", "ONG / Asociación"),
    ("publica", "Entidad pública"),
    ("otra", "Otra"),
]

ruc_validator = RegexValidator(r"^\d{11}$", "El RUC debe tener 11 dígitos.")


class Empresa(models.Model):
    # Bloque A — Información de la empresa
    ruc = models.CharField("RUC", max_length=11, unique=True, validators=[ruc_validator])
    razon_social = models.CharField("razón social", max_length=255)
    nombre_comercial = models.CharField("nombre comercial", max_length=255, blank=True)
    tipo = models.CharField("tipo", max_length=20, choices=TIPOS_EMPRESA, blank=True)
    ciiu = models.CharField("CIIU", max_length=120, blank=True)
    telefono = models.CharField("teléfono", max_length=40, blank=True)
    direccion = models.CharField("dirección", max_length=255, blank=True)
    web = models.URLField("web", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    # Imagen subida (persistida en el volumen de MEDIA_ROOT) o, alternativamente,
    # un enlace externo. La subida tiene prioridad (ver logo_src / banner_src).
    logo_img = models.ImageField("logo (imagen)", upload_to="empresas/logos/", blank=True)
    banner_img = models.ImageField("banner (imagen)", upload_to="empresas/banners/", blank=True)
    # Acepta una URL externa o una ruta interna (p. ej. /static/... del seed),
    # por eso es CharField y no URLField. La imagen subida tiene prioridad.
    logo_url = models.CharField("logo (URL o ruta)", max_length=300, blank=True)
    banner_url = models.CharField("banner (URL o ruta)", max_length=300, blank=True)
    video_url = models.URLField("video (URL)", blank=True)
    descripcion = models.TextField("descripción", blank=True)

    estado = models.CharField(
        "estado", max_length=20, choices=ESTADOS_EMPRESA, default=ESTADO_PENDIENTE
    )
    creado_en = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
        ordering = ["razon_social"]

    def __str__(self):
        return self.nombre_comercial or self.razon_social

    @property
    def logo_src(self) -> str:
        """URL del logo para mostrar: prioriza la imagen subida; si no, el enlace."""
        if self.logo_img:
            return self.logo_img.url
        return self.logo_url

    @property
    def banner_src(self) -> str:
        """URL del banner para mostrar: prioriza la imagen subida; si no, el enlace."""
        if self.banner_img:
            return self.banner_img.url
        return self.banner_url

    @property
    def es_referencial(self) -> bool:
        """Empresa sin cuenta de reclutador vinculada (la creó el admin)."""
        return not hasattr(self, "reclutador")

    @property
    def verificada(self) -> bool:
        """Badge «Verificada» = activa AND con reclutador (modelo-datos.md)."""
        return self.estado == ESTADO_ACTIVA and not self.es_referencial

    @property
    def puede_publicar(self) -> bool:
        """Solo una empresa activa puede publicar convocatorias (CA-2)."""
        return self.estado == ESTADO_ACTIVA


class Reclutador(models.Model):
    """Persona que gestiona las convocatorias de una empresa (1 por empresa, MVP / CA-5)."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reclutador",
        verbose_name="usuario",
    )
    empresa = models.OneToOneField(
        Empresa, on_delete=models.CASCADE, related_name="reclutador", verbose_name="empresa"
    )
    dni = models.CharField("DNI", max_length=8, blank=True)
    nombres = models.CharField("nombres", max_length=120)
    ap_paterno = models.CharField("apellido paterno", max_length=120)
    ap_materno = models.CharField("apellido materno", max_length=120, blank=True)
    cargo = models.CharField("cargo", max_length=120, blank=True)
    email = models.EmailField("email", blank=True)
    telefono = models.CharField("teléfono / celular", max_length=40, blank=True)

    class Meta:
        verbose_name = "reclutador"
        verbose_name_plural = "reclutadores"

    def __str__(self):
        return f"{self.nombres} {self.ap_paterno} — {self.empresa}"
