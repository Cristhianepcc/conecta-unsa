"""Tests de la feature 00-fundacion (criterios EARS)."""

import os

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

from apps.core.models import (
    AdminAllowlist,
    ParametroLegal,
    PesoTransparencia,
    ReglaElegibilidad,
)


class FundacionTests(TestCase):
    def test_ca1__home_responde_200(self):
        """CA-1: el proyecto arranca y responde 200 en `/`."""
        resp = self.client.get(reverse("core:home"))
        self.assertEqual(resp.status_code, 200)

    def test_ca2__lee_database_url(self):
        """CA-2: la base de datos se configura desde DATABASE_URL (Postgres)."""
        self.assertIn("postgresql", settings.DATABASES["default"]["ENGINE"])
        self.assertTrue(os.environ.get("DATABASE_URL"))

    def test_ca4__locale_es_lima_pen(self):
        """CA-4: opera en es / America/Lima / PEN."""
        self.assertEqual(settings.LANGUAGE_CODE, "es")
        self.assertEqual(settings.TIME_ZONE, "America/Lima")
        self.assertEqual(settings.CURRENCY_CODE, "PEN")

    def test_ca5__apps_instaladas(self):
        """CA-5: incluye las 7 apps del proyecto."""
        esperadas = {
            "apps.core",
            "apps.taxonomia",
            "apps.usuarios",
            "apps.empresas",
            "apps.convocatorias",
            "apps.matching",
            "apps.notificaciones",
        }
        instaladas = {cfg.name for cfg in apps.get_app_configs()}
        self.assertTrue(esperadas.issubset(instaladas))

    def test_ca6__config_as_data_en_admin(self):
        """CA-6: las 4 tablas config-as-data están registradas en Django Admin."""
        for modelo in (ParametroLegal, PesoTransparencia, ReglaElegibilidad, AdminAllowlist):
            self.assertIn(modelo, admin.site._registry)

    def test_ca6__config_as_data_persisten(self):
        """CA-6: las tablas config-as-data son utilizables (CRUD básico)."""
        ParametroLegal.objects.create(clave="rmv", valor="1130")
        PesoTransparencia.objects.create(criterio="banda_salarial", peso=30)
        ReglaElegibilidad.objects.create(
            estado_academico="egresado", tipo_convocatoria="empleo", permitido=True
        )
        AdminAllowlist.objects.create(email="admin@unsa.edu.pe")
        self.assertEqual(ParametroLegal.objects.count(), 1)
        self.assertEqual(PesoTransparencia.objects.get().peso, 30)
        self.assertTrue(ReglaElegibilidad.objects.get().permitido)
        self.assertEqual(AdminAllowlist.objects.get().email, "admin@unsa.edu.pe")
