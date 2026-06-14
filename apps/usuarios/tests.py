"""Tests de la feature 02-autenticacion (criterios EARS).

Se prueba el **ruteo de rol** y el control de acceso, no el handshake OAuth de
Google (estrategia-pruebas.md). El login con Google se simula con force_login.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import AdminAllowlist
from apps.usuarios.models import (
    ROL_ADMIN,
    ROL_EGRESADO,
    ROL_RECLUTADOR,
    Perfil,
)
from apps.usuarios.services import resolver_rol, resolver_rol_y_destino

User = get_user_model()


class RuteoRolTests(TestCase):
    def test_ca3__correo_en_allowlist_es_admin(self):
        """CA-3: un correo en AdminAllowlist se enruta al panel admin."""
        AdminAllowlist.objects.create(email="jefe@unsa.edu.pe")
        user = User.objects.create_user("jefe", email="jefe@unsa.edu.pe", password="x")
        self.assertEqual(resolver_rol(user), ROL_ADMIN)
        self.assertEqual(resolver_rol_y_destino(user), "core:panel_admin")

    def test_ca3__correo_fuera_de_allowlist_es_egresado(self):
        """CA-3: un correo fuera de la allowlist es egresado."""
        user = User.objects.create_user("ana", email="ana@gmail.com", password="x")
        self.assertEqual(resolver_rol(user), ROL_EGRESADO)

    def test_ca3__allowlist_case_insensitive(self):
        """CA-3: la allowlist no distingue mayúsculas/minúsculas."""
        AdminAllowlist.objects.create(email="Jefe@UNSA.edu.pe")
        user = User.objects.create_user("j2", email="jefe@unsa.edu.pe", password="x")
        self.assertEqual(resolver_rol(user), ROL_ADMIN)

    def test_ca2__primer_ingreso_va_a_completar_perfil(self):
        """CA-2: egresado sin perfil completo se enruta a completar-perfil."""
        user = User.objects.create_user("nuevo", email="nuevo@gmail.com", password="x")
        self.assertEqual(resolver_rol_y_destino(user), "usuarios:completar_perfil")

    def test__egresado_con_perfil_completo_va_a_dashboard(self):
        user = User.objects.create_user("vet", email="vet@gmail.com", password="x")
        user.perfil.perfil_completo = True
        user.perfil.save()
        self.assertEqual(resolver_rol_y_destino(user), "usuarios:dashboard")


class LoginEmpresaTests(TestCase):
    def test_ca4__empresa_entra_a_su_dashboard(self):
        """CA-4: empresa con credenciales válidas llega a su dashboard."""
        user = User.objects.create_user("empresa1", password="clave-segura-123")
        user.perfil.rol = ROL_RECLUTADOR
        user.perfil.save()

        resp = self.client.post(
            reverse("usuarios:login_empresa"),
            {"username": "empresa1", "password": "clave-segura-123"},
            follow=True,
        )
        self.assertRedirects(resp, reverse("empresas:dashboard"))

    def test_ca4__credenciales_invalidas_no_ingresan(self):
        """CA-4 (negativo): credenciales inválidas no autentican."""
        User.objects.create_user("empresa2", password="correcta")
        resp = self.client.post(
            reverse("usuarios:login_empresa"),
            {"username": "empresa2", "password": "incorrecta"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.wsgi_request.user.is_authenticated)


class ControlAccesoRolTests(TestCase):
    def test_ca5__egresado_no_entra_a_ruta_admin(self):
        """CA-5: un egresado recibe 403 al acceder al panel admin."""
        user = User.objects.create_user("eg", email="eg@gmail.com", password="x")
        self.client.force_login(user)
        resp = self.client.get(reverse("core:panel_admin"))
        self.assertEqual(resp.status_code, 403)

    def test_ca5__admin_si_entra_a_ruta_admin(self):
        AdminAllowlist.objects.create(email="adm@unsa.edu.pe")
        user = User.objects.create_user("adm", email="adm@unsa.edu.pe", password="x")
        resolver_rol(user)  # promueve a admin
        self.client.force_login(user)
        resp = self.client.get(reverse("core:panel_admin"))
        self.assertEqual(resp.status_code, 200)

    def test_ca5__anonimo_redirige_a_login(self):
        resp = self.client.get(reverse("usuarios:dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("usuarios:login"), resp.url)

    def test_ca5__egresado_no_entra_a_dashboard_empresa(self):
        user = User.objects.create_user("eg2", email="eg2@gmail.com", password="x")
        self.client.force_login(user)
        resp = self.client.get(reverse("empresas:dashboard"))
        self.assertEqual(resp.status_code, 403)


class ConsentimientoTests(TestCase):
    def test_ca6__captura_consentimiento(self):
        """CA-6: completar-perfil registra el consentimiento de datos."""
        user = User.objects.create_user("c", email="c@gmail.com", password="x")
        self.client.force_login(user)
        resp = self.client.post(
            reverse("usuarios:completar_perfil"), {"consentimiento": "on"}, follow=True
        )
        self.assertRedirects(resp, reverse("usuarios:dashboard"))
        perfil = Perfil.objects.get(user=user)
        self.assertTrue(perfil.consentimiento_datos)
        self.assertIsNotNone(perfil.consentimiento_en)
        self.assertTrue(perfil.perfil_completo)

    def test_ca6__sin_consentimiento_no_avanza(self):
        """CA-6 (negativo): sin marcar el checkbox no se completa el perfil."""
        user = User.objects.create_user("c2", email="c2@gmail.com", password="x")
        self.client.force_login(user)
        resp = self.client.post(reverse("usuarios:completar_perfil"), {})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Perfil.objects.get(user=user).consentimiento_datos)


class LoginRenderTests(TestCase):
    def test_ca1__login_muestra_dos_puertas(self):
        """CA-1: la pantalla de login ofrece la puerta de Google y la de empresa."""
        resp = self.client.get(reverse("usuarios:login"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Soy de la UNSA")
        self.assertContains(resp, "Soy empresa")

    def test__senal_crea_perfil_automaticamente(self):
        user = User.objects.create_user("auto", email="auto@gmail.com", password="x")
        self.assertTrue(Perfil.objects.filter(user=user).exists())
