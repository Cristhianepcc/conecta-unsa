"""Tests del adaptador de padrón y el endpoint de validación de DNI (Eje 2)."""

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .padron import consultar_dni, dni_valido

User = get_user_model()


class PadronTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_taxonomia")

    def test_dni_valido_formato(self):
        self.assertTrue(dni_valido("12345678"))
        self.assertFalse(dni_valido("123"))
        self.assertFalse(dni_valido("abcdefgh"))
        self.assertFalse(dni_valido(""))

    def test_consultar_dni_existente(self):
        r = consultar_dni("12345678")
        self.assertIsNotNone(r)
        self.assertEqual(r.carrera, "Ingeniería Industrial")
        self.assertEqual(r.estado_academico, "egresado")
        self.assertEqual(r.fuente, "UNSA")

    def test_consultar_dni_inexistente(self):
        self.assertIsNone(consultar_dni("00000000"))


class ValidarDniEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_taxonomia")
        cls.user = User.objects.create_user("egresado_test", password="x")
        cls.url = reverse("integraciones:validar_dni")

    def test_requiere_login(self):
        resp = self.client.get(self.url, {"dni": "12345678"})
        self.assertEqual(resp.status_code, 302)

    def test_validado(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.url, {"dni": "12345678"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["estado"], "validado")
        self.assertEqual(data["carrera"], "Ingeniería Industrial")
        self.assertIn("carrera_id", data)

    def test_no_encontrado(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.url, {"dni": "00000000"})
        self.assertEqual(resp.json()["estado"], "no_encontrado")

    def test_formato_invalido(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.url, {"dni": "abc"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["estado"], "formato_invalido")
