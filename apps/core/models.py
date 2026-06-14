"""Modelos config-as-data (constitución §1.2): reglas variables en tablas
editables por el admin, no en código (NFR-MNT-1)."""

from django.db import models

from . import constants


class ParametroLegal(models.Model):
    """Valores legales que cambian con el tiempo (RMV, topes, plazos)."""

    clave = models.CharField("clave", max_length=80, unique=True)
    valor = models.CharField("valor", max_length=255)
    descripcion = models.CharField("descripción", max_length=255, blank=True)
    actualizado_en = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        verbose_name = "parámetro legal"
        verbose_name_plural = "parámetros legales"
        ordering = ["clave"]

    def __str__(self):
        return f"{self.clave} = {self.valor}"


class PesoTransparencia(models.Model):
    """Peso de cada criterio del % de transparencia (suman 100)."""

    criterio = models.CharField("criterio", max_length=80, unique=True)
    etiqueta = models.CharField("etiqueta", max_length=255, blank=True)
    peso = models.PositiveIntegerField("peso")

    class Meta:
        verbose_name = "peso de transparencia"
        verbose_name_plural = "pesos de transparencia"
        ordering = ["-peso", "criterio"]

    def __str__(self):
        return f"{self.criterio} ({self.peso})"


class ReglaElegibilidad(models.Model):
    """Matriz de elegibilidad: estado académico × tipo de convocatoria."""

    estado_academico = models.CharField(
        "estado académico", max_length=20, choices=constants.ESTADOS_ACADEMICOS
    )
    tipo_convocatoria = models.CharField(
        "tipo de convocatoria", max_length=40, choices=constants.TIPOS_CONVOCATORIA
    )
    permitido = models.BooleanField("permitido", default=True)

    class Meta:
        verbose_name = "regla de elegibilidad"
        verbose_name_plural = "matriz de elegibilidad"
        unique_together = [("estado_academico", "tipo_convocatoria")]
        ordering = ["estado_academico", "tipo_convocatoria"]

    def __str__(self):
        marca = "✓" if self.permitido else "✗"
        return f"{self.estado_academico} × {self.tipo_convocatoria} {marca}"


class AdminAllowlist(models.Model):
    """Correos autorizados a obtener el rol administrativo (NFR-SEC-4)."""

    email = models.EmailField("correo", unique=True)
    nota = models.CharField("nota", max_length=255, blank=True)
    creado_en = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        verbose_name = "correo administrativo (allowlist)"
        verbose_name_plural = "allowlist de administrativos"
        ordering = ["email"]

    def __str__(self):
        return self.email
