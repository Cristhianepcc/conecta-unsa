"""Taxonomía académica UNSA: Área → Facultad → Carrera + GrupoAfin.

Config-as-data: toda la jerarquía es editable por el admin (constitución §1.2).
Modelo coherente con specs/modelo-datos.md y specs/01-taxonomia/design.md.
"""

from django.db import models


class Area(models.Model):
    """Nivel más alto de la taxonomía UNSA (3 en total)."""

    nombre = models.CharField("nombre", max_length=120, unique=True)
    orden = models.PositiveIntegerField("orden", default=0)

    class Meta:
        verbose_name = "área"
        verbose_name_plural = "áreas"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


class Facultad(models.Model):
    """Subdivisión de un Área (16 en total)."""

    nombre = models.CharField("nombre", max_length=160, unique=True)
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name="facultades", verbose_name="área"
    )

    class Meta:
        verbose_name = "facultad"
        verbose_name_plural = "facultades"
        ordering = ["area__orden", "nombre"]

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    """Programa académico (43). Unidad atómica del matching (Gate 2)."""

    nombre = models.CharField("nombre", max_length=160, unique=True)
    facultad = models.ForeignKey(
        Facultad, on_delete=models.PROTECT, related_name="carreras", verbose_name="facultad"
    )
    activa = models.BooleanField("activa", default=True)

    class Meta:
        verbose_name = "carrera"
        verbose_name_plural = "carreras"
        ordering = ["facultad__area__orden", "facultad__nombre", "nombre"]

    def __str__(self):
        return self.nombre

    @property
    def area(self):
        return self.facultad.area


class GrupoAfin(models.Model):
    """Conjunto nombrado de carreras «o afines», editable por el admin."""

    nombre = models.CharField("nombre", max_length=160, unique=True)
    carreras = models.ManyToManyField(
        Carrera, related_name="grupos_afines", verbose_name="carreras"
    )

    class Meta:
        verbose_name = "grupo afín"
        verbose_name_plural = "grupos afines"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
