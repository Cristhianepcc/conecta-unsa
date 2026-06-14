"""Tests de la feature 10-dashboard-estudiante (criterios EARS)."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.core import constants
from apps.empresas.models import ESTADO_ACTIVA, Empresa
from apps.taxonomia.models import Carrera
from apps.usuarios.models import PerfilTalento

from .interacciones import esta_guardada, guardadas_de, historial_de
from .models import (
    ESTADO_PUBLICADA,
    INTERACCION_VISTA,
    Convocatoria,
    InteraccionConvocatoria,
)

User = get_user_model()


class BaseDashboard(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_config")
        call_command("seed_taxonomia")
        call_command("seed_elegibilidad")
        cls.empresa = Empresa.objects.create(
            ruc="21000000001", razon_social="Dash SAC", estado=ESTADO_ACTIVA
        )
        cls.sistemas = Carrera.objects.get(nombre="Ingeniería de Sistemas")
        cls.medicina = Carrera.objects.get(nombre="Medicina")

    def _conv(self, titulo, carreras, tipo=constants.TIPO_EMPLEO):
        conv = Convocatoria.objects.create(
            empresa=self.empresa, tipo=tipo, titulo=titulo, estado=ESTADO_PUBLICADA,
            transparencia_pct=70, medio_postulacion="https://acme.pe/aplica",
            fecha_limite=date.today() + timedelta(days=15),
        )
        conv.carreras_objetivo.set(carreras)
        return conv

    def _login_egresado(self, carrera=None):
        user = User.objects.create_user("egre", email="egre@gmail.com", password="x")
        talento, _ = PerfilTalento.objects.get_or_create(usuario=user)
        talento.carrera = carrera or self.sistemas
        talento.estado_academico = "egresado"
        talento.save()
        self.client.force_login(user)
        return user


class FeedTests(BaseDashboard):
    def test_ca1__dashboard_muestra_solo_elegibles(self):
        """CA-1: el dashboard muestra el feed (elegibles para la carrera)."""
        self._conv("Para Sistemas", [self.sistemas])
        self._conv("Para Medicina", [self.medicina])
        self._login_egresado(self.sistemas)
        resp = self.client.get(reverse("usuarios:dashboard"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Para Sistemas")
        self.assertNotContains(resp, "Para Medicina")

    def test_ca2__tarjeta_muestra_transparencia(self):
        self._conv("Para Sistemas", [self.sistemas])
        self._login_egresado(self.sistemas)
        resp = self.client.get(reverse("usuarios:dashboard"))
        self.assertContains(resp, "70%")


class PostularTests(BaseDashboard):
    def test_ca3__postular_redirige_y_registra_vista(self):
        """CA-3: postular redirige al medio externo y registra la vista."""
        conv = self._conv("Empleo", [self.sistemas])
        user = self._login_egresado(self.sistemas)
        resp = self.client.get(reverse("convocatorias:postular", args=[conv.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, "https://acme.pe/aplica")
        self.assertTrue(
            InteraccionConvocatoria.objects.filter(
                usuario=user, convocatoria=conv, tipo=INTERACCION_VISTA
            ).exists()
        )

    def test_ca3__ver_detalle_registra_vista(self):
        conv = self._conv("Empleo", [self.sistemas])
        user = self._login_egresado(self.sistemas)
        self.client.get(reverse("convocatorias:detalle", args=[conv.id]))
        self.assertIn(conv, list(historial_de(user)))

    def test_ca3__postular_por_correo_abre_mailto(self):
        """Si la empresa solo deja un correo, postular abre un mailto con asunto."""
        conv = self._conv("Empleo correo", [self.sistemas])
        conv.medio_postulacion = "rrhh@empresa.pe"
        conv.save(update_fields=["medio_postulacion"])
        self._login_egresado(self.sistemas)
        resp = self.client.get(reverse("convocatorias:postular", args=[conv.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith("mailto:rrhh@empresa.pe?subject="))


class GuardarTests(BaseDashboard):
    def test_ca4__guardar_y_listar(self):
        """CA-4: guardar una convocatoria y verla en guardadas (toggle)."""
        conv = self._conv("Empleo", [self.sistemas])
        user = self._login_egresado(self.sistemas)

        self.client.post(reverse("convocatorias:guardar", args=[conv.id]))
        self.assertTrue(esta_guardada(user, conv))
        self.assertIn(conv, list(guardadas_de(user)))

        # Toggle: guardar de nuevo la quita.
        self.client.post(reverse("convocatorias:guardar", args=[conv.id]))
        self.assertFalse(esta_guardada(user, conv))

    def test_ca4__historial_y_guardadas_paginas(self):
        conv = self._conv("Empleo", [self.sistemas])
        self._login_egresado(self.sistemas)
        self.client.post(reverse("convocatorias:guardar", args=[conv.id]))
        self.assertContains(self.client.get(reverse("usuarios:guardadas")), "Empleo")
        self.client.get(reverse("convocatorias:detalle", args=[conv.id]))
        self.assertContains(self.client.get(reverse("usuarios:historial")), "Empleo")
