"""Tests de la feature 02-autenticacion (criterios EARS).

Se prueba el **ruteo de rol** y el control de acceso, no el handshake OAuth de
Google (estrategia-pruebas.md). El login con Google se simula con force_login.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
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
    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command

        call_command("seed_taxonomia")

    def test_ca6__captura_consentimiento(self):
        """CA-6: completar-perfil registra el consentimiento de datos (con carrera + estado)."""
        from apps.taxonomia.models import Carrera

        user = User.objects.create_user("c", email="c@gmail.com", password="x")
        self.client.force_login(user)
        resp = self.client.post(
            reverse("usuarios:completar_perfil"),
            {
                "carrera": Carrera.objects.first().id,
                "estado_academico": "egresado",
                "consentimiento": "on",
                "consentimiento_matching": "on",
            },
            follow=True,
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


class DemoLoginTests(TestCase):
    """Accesos directos de demo (DEMO_MODE) para mostrar los flujos al jurado."""

    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command

        call_command("seed_taxonomia")

    @override_settings(DEMO_MODE=True)
    def test_demo_egresado_enruta_a_dashboard(self):
        resp = self.client.get(reverse("usuarios:demo_login", args=["egresado"]), follow=True)
        self.assertRedirects(resp, reverse("usuarios:dashboard"))
        self.assertEqual(User.objects.get(username="demo_egresado").perfil.rol, ROL_EGRESADO)

    @override_settings(DEMO_MODE=True)
    def test_demo_admin_enruta_a_panel(self):
        resp = self.client.get(reverse("usuarios:demo_login", args=["admin"]), follow=True)
        self.assertRedirects(resp, reverse("core:panel_admin"))
        self.assertEqual(User.objects.get(username="demo_admin").perfil.rol, ROL_ADMIN)

    @override_settings(DEMO_MODE=False)
    def test_demo_apagado_da_404(self):
        resp = self.client.get(reverse("usuarios:demo_login", args=["egresado"]))
        self.assertEqual(resp.status_code, 404)


# --- 07 Perfil de talento y credencial pública ------------------------------
class PerfilTalentoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command

        call_command("seed_taxonomia")

    def _login_egresado(self, username="egre"):
        user = User.objects.create_user(username, email=f"{username}@gmail.com", password="x")
        self.client.force_login(user)
        return user

    def test_ca1__completar_perfil_pide_carrera_y_estado(self):
        """CA-1: el primer ingreso captura carrera y estado académico."""
        from apps.taxonomia.models import Carrera

        from .models import PerfilTalento

        self._login_egresado()
        carrera = Carrera.objects.first()
        resp = self.client.post(
            reverse("usuarios:completar_perfil"),
            {
                "carrera": carrera.id,
                "estado_academico": "egresado",
                "consentimiento": "on",
                "consentimiento_matching": "on",
            },
            follow=True,
        )
        self.assertRedirects(resp, reverse("usuarios:dashboard"))
        talento = PerfilTalento.objects.get(usuario__username="egre")
        self.assertEqual(talento.carrera, carrera)
        self.assertEqual(talento.estado_academico, "egresado")

    def test_ca2__agregar_credencial_autodeclarada(self):
        """CA-2: el egresado puede agregar credenciales autodeclaradas."""
        from .models import FUENTE_AUTODECLARADO, Credencial

        self._login_egresado()
        self.client.post(
            reverse("usuarios:perfil"),
            {"agregar_credencial": "1", "tipo": "idioma", "detalle": "Inglés B2"},
        )
        cred = Credencial.objects.get(detalle="Inglés B2")
        self.assertEqual(cred.fuente, FUENTE_AUTODECLARADO)
        self.assertTrue(cred.editable)

    def test_ca3__credencial_verificada_no_editable(self):
        """CA-3: una credencial verificada es solo lectura (no se elimina)."""
        from .models import FUENTE_VERIFICADO, Credencial
        from .services import asegurar_perfil_talento

        user = self._login_egresado()
        talento = asegurar_perfil_talento(user)
        cred = Credencial.objects.create(
            perfil=talento, tipo="tesis", detalle="Tesis X", fuente=FUENTE_VERIFICADO
        )
        self.assertFalse(cred.editable)
        resp = self.client.post(
            reverse("usuarios:eliminar_credencial", args=[cred.id]), follow=True
        )
        self.assertTrue(Credencial.objects.filter(pk=cred.id).exists())  # no se borró
        self.assertContains(resp, "no se pueden editar")

    def test_ca4__preferencias_se_guardan(self):
        """CA-4: preferencias (frecuencia, silenciar, tipos) se persisten."""
        from apps.taxonomia.models import Carrera

        from .services import asegurar_perfil_talento

        user = self._login_egresado()
        carrera = Carrera.objects.first()
        self.client.post(
            reverse("usuarios:perfil"),
            {
                "guardar_preferencias": "1",
                "carrera": carrera.id,
                "estado_academico": "egresado",
                "frecuencia": "semanal",
                # Matriz tri-estado: cada tipo lleva su estado.
                "tipo_voluntariado": "silenciado",
                "tipo_practica_preprofesional": "preferido",
            },
        )
        talento = asegurar_perfil_talento(user)
        talento.refresh_from_db()
        self.assertEqual(talento.frecuencia, "semanal")
        self.assertIn("voluntariado", talento.categorias_silenciadas)
        self.assertIn("practica_preprofesional", talento.tipos_preferidos)

    def test_ca5_ca6__activar_genera_url_y_sirve_noindex(self):
        """CA-5/CA-6: activar genera /credencial/<slug>; se sirve con noindex."""
        from .services import asegurar_perfil_talento

        user = self._login_egresado()
        self.client.post(reverse("usuarios:credencial_config"), {"accion": "activar"})
        talento = asegurar_perfil_talento(user)
        talento.refresh_from_db()
        self.assertTrue(talento.cred_activa)
        self.assertTrue(talento.cred_slug)

        self.client.logout()
        resp = self.client.get(reverse("usuarios:credencial_publica", args=[talento.cred_slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["X-Robots-Tag"], "noindex, nofollow")
        self.assertContains(resp, "noindex")

    def test_ca7__revocar_apaga_la_url(self):
        """CA-7: revocar desactiva el acceso público (404 por el enlace)."""
        from .services import activar_credencial_publica, asegurar_perfil_talento

        user = self._login_egresado()
        talento = asegurar_perfil_talento(user)
        slug = activar_credencial_publica(talento)

        self.client.post(reverse("usuarios:credencial_config"), {"accion": "revocar"})
        self.client.logout()
        resp = self.client.get(reverse("usuarios:credencial_publica", args=[slug]))
        self.assertEqual(resp.status_code, 404)


# --- Ayuda (P0) -------------------------------------------------------------
class AyudaTests(TestCase):
    def test__egresado_ve_ayuda_con_faq(self):
        """El egresado accede a la ayuda con guía rápida y preguntas frecuentes."""
        user = User.objects.create_user("eg_ayuda", email="eg_ayuda@gmail.com", password="x")
        self.client.force_login(user)
        resp = self.client.get(reverse("usuarios:ayuda"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Preguntas frecuentes")

    def test__reclutador_no_entra_a_ayuda_de_egresado(self):
        """La ayuda del egresado es exclusiva de su rol."""
        user = User.objects.create_user("recl_ayuda", password="x")
        user.perfil.rol = ROL_RECLUTADOR
        user.perfil.save()
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("usuarios:ayuda")).status_code, 403)
