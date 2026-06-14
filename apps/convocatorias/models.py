"""Convocatoria: entidad central (8 tipos, 3 niveles). modelo-datos.md §1-§6.

Una sola tabla con todos los campos; Nivel 2 y 3 son nullable. El formulario decide
qué mostrar/exigir según `tipo` (feature 11/12). Aquí viven el modelo, los estados
y el % de transparencia.
"""

from django.conf import settings
from django.db import models

from apps.core import constants
from apps.empresas.models import Empresa
from apps.taxonomia.models import Carrera

# --- Enumeraciones ----------------------------------------------------------
MODALIDAD_PRESENCIAL = "presencial"
MODALIDAD_REMOTO = "remoto"
MODALIDAD_HIBRIDO = "hibrido"
MODALIDADES = [
    (MODALIDAD_PRESENCIAL, "Presencial"),
    (MODALIDAD_REMOTO, "Remoto"),
    (MODALIDAD_HIBRIDO, "Híbrido"),
]

CREADA_POR_EMPRESA = "empresa"
CREADA_POR_ADMIN = "admin"
CREADA_POR = [
    (CREADA_POR_EMPRESA, "Empresa"),
    (CREADA_POR_ADMIN, "Administrativo"),
]

ESTADO_BORRADOR = "borrador"
ESTADO_PENDIENTE = "pendiente"
ESTADO_PUBLICADA = "publicada"
ESTADO_OBSERVADA = "observada"
ESTADO_RECHAZADA = "rechazada"
ESTADO_CADUCADA = "caducada"
ESTADOS = [
    (ESTADO_BORRADOR, "Borrador"),
    (ESTADO_PENDIENTE, "Pendiente de revisión"),
    (ESTADO_PUBLICADA, "Publicada"),
    (ESTADO_OBSERVADA, "Observada"),
    (ESTADO_RECHAZADA, "Rechazada"),
    (ESTADO_CADUCADA, "Caducada"),
]

# Etiquetas del semáforo de transparencia (modelo-datos.md §6).
TRANSPARENCIA_ALTA = "alta"
TRANSPARENCIA_MEDIA = "media"
TRANSPARENCIA_BAJA = "baja"


class Convocatoria(models.Model):
    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, related_name="convocatorias", verbose_name="empresa"
    )
    creada_por = models.CharField(
        "creada por", max_length=10, choices=CREADA_POR, default=CREADA_POR_EMPRESA
    )
    tipo = models.CharField("tipo", max_length=40, choices=constants.TIPOS_CONVOCATORIA)

    # --- Nivel 1 — Fundamentales ---
    titulo = models.CharField("título del puesto", max_length=255)
    descripcion = models.TextField("descripción y requisitos", blank=True)
    modalidad = models.CharField("modalidad", max_length=20, choices=MODALIDADES, blank=True)
    ubicacion = models.CharField("ubicación", max_length=160, blank=True)
    duracion_estimada = models.CharField("duración estimada", max_length=120, blank=True)
    fecha_limite = models.DateField("fecha límite de postulación", null=True, blank=True)
    medio_postulacion = models.CharField("cómo postular (URL o email)", max_length=255, blank=True)
    email_contacto = models.EmailField("email de contacto", blank=True)
    no_discriminacion = models.BooleanField("declaración de no discriminación", default=False)

    # --- Nivel 2 — Obligatorios según tipo (nullable) ---
    subvencion_remuneracion = models.DecimalField(
        "subvención / remuneración / honorario (S/)", max_digits=10, decimal_places=2,
        null=True, blank=True,
    )
    jornada_horas = models.PositiveIntegerField("jornada (h/sem)", null=True, blank=True)
    requiere_convenio = models.BooleanField("requiere convenio UNSA", null=True, blank=True)
    ciclo_minimo = models.PositiveIntegerField("ciclo/semestre mínimo", null=True, blank=True)
    tiempo_egreso_meses = models.PositiveIntegerField(
        "tiempo máx. de egreso (meses)", null=True, blank=True
    )
    regimen = models.CharField("régimen laboral", max_length=120, blank=True)
    bases_url = models.URLField("bases + cronograma (URL)", blank=True)
    cronograma = models.TextField("cronograma", blank=True)
    entidad_otorgante = models.CharField("entidad otorgante", max_length=160, blank=True)
    no_vinculo = models.BooleanField('disclaimer "no genera vínculo laboral"', default=False)
    incluye_seguro = models.BooleanField("incluye EsSalud / seguro", null=True, blank=True)

    # --- Nivel 3 — Opcionales (mejora progresiva, nullable) ---
    banda_salarial_min = models.DecimalField(
        "banda salarial mín. (S/)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    banda_salarial_max = models.DecimalField(
        "banda salarial máx. (S/)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    salario_confidencial = models.BooleanField("salario confidencial", default=False)
    vacantes = models.PositiveIntegerField("n.º de vacantes", null=True, blank=True)
    beneficios = models.TextField("beneficios", blank=True)
    discapacidad = models.BooleanField("abierta a personas con discapacidad", default=False)

    # --- Segmentación / estado / transparencia ---
    carreras_objetivo = models.ManyToManyField(
        Carrera, related_name="convocatorias", verbose_name="carreras objetivo", blank=True
    )
    estado = models.CharField("estado", max_length=20, choices=ESTADOS, default=ESTADO_BORRADOR)
    transparencia_pct = models.PositiveIntegerField("transparencia (%)", default=0)

    # Flujo admin (feature 06)
    comentario_revision = models.TextField("comentario de revisión", blank=True)
    fecha_publicacion = models.DateTimeField("fecha de publicación", null=True, blank=True)

    creada_en = models.DateTimeField("creada", auto_now_add=True)
    actualizada_en = models.DateTimeField("actualizada", auto_now=True)

    class Meta:
        verbose_name = "convocatoria"
        verbose_name_plural = "convocatorias"
        ordering = ["-creada_en"]

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

    @property
    def etiqueta_transparencia(self) -> str:
        if self.transparencia_pct >= 80:
            return TRANSPARENCIA_ALTA
        if self.transparencia_pct >= 50:
            return TRANSPARENCIA_MEDIA
        return TRANSPARENCIA_BAJA

    @property
    def es_voluntariado(self) -> bool:
        return self.tipo == constants.TIPO_VOLUNTARIADO

    @property
    def dias_para_cierre(self):
        """Días que faltan para la fecha límite (None si no hay; negativo si ya pasó)."""
        if self.fecha_limite is None:
            return None
        from django.utils import timezone

        return (self.fecha_limite - timezone.localdate()).days

    @property
    def cierra_pronto(self) -> bool:
        """True si cierra en 3 días o menos (y aún no venció)."""
        d = self.dias_para_cierre
        return d is not None and 0 <= d <= 3

    @property
    def medio_efectivo(self) -> str:
        """Medio de postulación; si no hay, cae al email de contacto."""
        return self.medio_postulacion or self.email_contacto or ""

    @property
    def medio_es_correo(self) -> bool:
        """True si el medio de postulación es un correo (no una URL)."""
        m = self.medio_efectivo
        return bool(m) and "@" in m and not m.lower().startswith("http")

    @property
    def activa(self) -> bool:
        """Publicada y aún dentro de su fecha límite (flujo-admin.md §1)."""
        from django.utils import timezone

        if self.estado != ESTADO_PUBLICADA:
            return False
        if self.fecha_limite is None:
            return True
        return self.fecha_limite >= timezone.localdate()

    def recalcular_transparencia(self, guardar: bool = True) -> int:
        """Recalcula y (opcionalmente) persiste `transparencia_pct`."""
        from .services import calcular_transparencia

        self.transparencia_pct = calcular_transparencia(self)
        if guardar and self.pk:
            super().save(update_fields=["transparencia_pct"])
        return self.transparencia_pct


# --- Interacción del egresado con convocatorias (feature 10) ----------------
INTERACCION_VISTA = "vista"
INTERACCION_GUARDADA = "guardada"
TIPOS_INTERACCION = [
    (INTERACCION_VISTA, "Vista"),
    (INTERACCION_GUARDADA, "Guardada"),
]


class InteraccionConvocatoria(models.Model):
    """Vista o guardado de una convocatoria por un egresado (historial / métricas)."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="interacciones", verbose_name="usuario",
    )
    convocatoria = models.ForeignKey(
        Convocatoria, on_delete=models.CASCADE,
        related_name="interacciones", verbose_name="convocatoria",
    )
    tipo = models.CharField("tipo", max_length=10, choices=TIPOS_INTERACCION)
    creado_en = models.DateTimeField("creado", auto_now=True)

    class Meta:
        verbose_name = "interacción con convocatoria"
        verbose_name_plural = "interacciones con convocatorias"
        unique_together = [("usuario", "convocatoria", "tipo")]
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.usuario} {self.tipo} {self.convocatoria_id}"
