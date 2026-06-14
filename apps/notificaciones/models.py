"""Notificaciones in-app y log del resumen semanal (feature 08; notificaciones.md)."""

from django.conf import settings
from django.db import models

TIPO_NUEVA_PERTINENTE = "nueva_pertinente"
TIPO_OBSERVADA = "observada"
TIPO_FECHA_LIMITE = "fecha_limite"
TIPO_RESUMEN = "resumen"
TIPO_GENERAL = "general"

TIPOS_NOTIFICACION = [
    (TIPO_NUEVA_PERTINENTE, "Nueva convocatoria pertinente"),
    (TIPO_OBSERVADA, "Convocatoria observada"),
    (TIPO_FECHA_LIMITE, "Fecha límite próxima"),
    (TIPO_RESUMEN, "Resumen disponible"),
    (TIPO_GENERAL, "General"),
]


class Notificacion(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="notificaciones", verbose_name="usuario",
    )
    tipo = models.CharField("tipo", max_length=30, choices=TIPOS_NOTIFICACION, default=TIPO_GENERAL)
    mensaje = models.CharField("mensaje", max_length=255)
    url = models.CharField("URL", max_length=255, blank=True)
    leido = models.BooleanField("leído", default=False)
    creado_en = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        verbose_name = "notificación"
        verbose_name_plural = "notificaciones"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.get_tipo_display()} → {self.usuario}"


class ResumenSemanalLog(models.Model):
    """Registro de auditoría de cada resumen enviado (CA-6)."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="resumenes", verbose_name="usuario",
    )
    convocatorias = models.ManyToManyField(
        "convocatorias.Convocatoria", related_name="resumenes", verbose_name="convocatorias"
    )
    enviado_en = models.DateTimeField("enviado", auto_now_add=True)

    class Meta:
        verbose_name = "log de resumen semanal"
        verbose_name_plural = "logs de resúmenes semanales"
        ordering = ["-enviado_en"]

    def __str__(self):
        return f"Resumen a {self.usuario} ({self.enviado_en:%Y-%m-%d})"
