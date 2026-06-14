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


# --- 09 Landing pública -----------------------------------------------------
class LandingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from datetime import date, timedelta

        from django.core.management import call_command

        from apps.convocatorias.models import ESTADO_PUBLICADA, Convocatoria
        from apps.empresas.models import ESTADO_ACTIVA, Empresa
        from apps.taxonomia.models import Carrera

        call_command("seed_config")
        call_command("seed_taxonomia")
        empresa = Empresa.objects.create(
            ruc="20900000001", razon_social="Landing SAC", estado=ESTADO_ACTIVA
        )
        sistemas = Carrera.objects.get(nombre="Ingeniería de Sistemas")
        for i in range(3):
            conv = Convocatoria.objects.create(
                empresa=empresa, tipo="empleo", titulo=f"Empleo {i}",
                estado=ESTADO_PUBLICADA, transparencia_pct=80,
                fecha_limite=date.today() + timedelta(days=20),
            )
            conv.carreras_objetivo.set([sistemas])
        cls.sistemas = sistemas

    def test_ca1__metricas_calculadas_de_bd(self):
        """CA-1: las métricas se calculan de datos reales, no son constantes."""
        from apps.core.services import metricas_landing

        m = metricas_landing()
        self.assertEqual(m["convocatorias_activas"], 3)
        self.assertEqual(m["indice_transparencia"], 80)
        self.assertGreaterEqual(m["carreras_cubiertas"], 1)

    def test_ca1__metricas_cambian_con_los_datos(self):
        """CA-1: si cambian los datos, cambia la métrica (no es un número fijo)."""
        from apps.convocatorias.models import ESTADO_PUBLICADA, Convocatoria
        from apps.core.services import metricas_landing
        from datetime import date, timedelta

        antes = metricas_landing()["convocatorias_activas"]
        c = Convocatoria.objects.create(
            empresa_id=Convocatoria.objects.first().empresa_id, tipo="empleo",
            titulo="Nueva", estado=ESTADO_PUBLICADA,
            fecha_limite=date.today() + timedelta(days=5),
        )
        c.carreras_objetivo.set([self.sistemas])
        self.assertEqual(metricas_landing()["convocatorias_activas"], antes + 1)

    def test_ca2__dos_puertas_en_landing(self):
        """CA-2: la landing ofrece entrada para egresado y para empresa."""
        resp = self.client.get(reverse("core:home"))
        # Dos puertas de acceso en la landing (egresado y empresa).
        self.assertContains(resp, "Egresado")
        self.assertContains(resp, "Empresa")
        self.assertContains(resp, reverse("usuarios:login"))
        self.assertContains(resp, reverse("empresas:registro"))

    def test_ca3__categorias_desde_taxonomia(self):
        """CA-3: las categorías provienen de la taxonomía real con conteos reales."""
        from apps.core.services import categorias_con_conteo, categorias_profesionales

        # Helper a nivel de área (3 áreas).
        self.assertEqual(len(categorias_con_conteo()), 3)

        # Tiles de la landing: 7 categorías profesionales con conteos reales.
        tiles = categorias_profesionales()
        self.assertEqual(len(tiles), 7)
        labels = {t["label"] for t in tiles}
        self.assertIn("Ingenierías", labels)
        # La categoría "Ingenierías" agrupa la carrera sembrada (Ing. de Sistemas).
        ingenierias = next(t for t in tiles if t["label"] == "Ingenierías")
        self.assertGreaterEqual(ingenierias["conteo"], 1)
        resp = self.client.get(reverse("core:home"))
        self.assertContains(resp, "Ingenierías")

    def test_ca4__transparencia_explicada(self):
        """CA-4: la landing comunica la transparencia/verificación y el índice real."""
        resp = self.client.get(reverse("core:home"))
        self.assertContains(resp, "Convocatorias verificadas")
        self.assertContains(resp, "información transparente")
        self.assertContains(resp, "80%")  # índice de transparencia calculado del seed

    def test_ca5__footer_institucional(self):
        """CA-5: footer con privacidad, términos y contacto."""
        resp = self.client.get(reverse("core:home"))
        self.assertContains(resp, reverse("core:privacidad"))
        self.assertContains(resp, reverse("core:terminos"))
        self.assertContains(resp, "empleabilidad@unsa.edu.pe")

    def test__paginas_apoyo_responden(self):
        for nombre in ("como_funciona", "privacidad", "terminos"):
            self.assertEqual(self.client.get(reverse(f"core:{nombre}")).status_code, 200)
