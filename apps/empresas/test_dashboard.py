"""Tests de la feature 11-dashboard-empresa (criterios EARS)."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.core import constants
from apps.convocatorias.models import (
    CREADA_POR_EMPRESA,
    ESTADO_OBSERVADA,
    ESTADO_PENDIENTE,
    ESTADO_PUBLICADA,
    Convocatoria,
)
from apps.taxonomia.models import Carrera

from .models import ESTADO_ACTIVA, ESTADO_PENDIENTE as EMP_PENDIENTE, Empresa, Reclutador

User = get_user_model()


class BaseEmpresaDash(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_config")
        call_command("seed_taxonomia")
        call_command("seed_elegibilidad")
        cls.sistemas = Carrera.objects.get(nombre="Ingeniería de Sistemas")

    _ruc = 22000000000

    def _empresa_con_login(self, estado=ESTADO_ACTIVA, username="recl"):
        from apps.usuarios.models import ROL_RECLUTADOR

        BaseEmpresaDash._ruc += 1
        empresa = Empresa.objects.create(
            ruc=str(BaseEmpresaDash._ruc), razon_social="Empresa Dash", estado=estado
        )
        user = User.objects.create_user(username, password="x")
        user.perfil.rol = ROL_RECLUTADOR
        user.perfil.save()
        Reclutador.objects.create(usuario=user, empresa=empresa, nombres="R", ap_paterno="X")
        self.client.force_login(user)
        return empresa

    def _datos_conv(self, **kw):
        datos = dict(
            tipo=constants.TIPO_EMPLEO,
            titulo="Analista",
            descripcion="x" * 120,
            modalidad="remoto",
            ubicacion="Arequipa",
            duracion_estimada="6 meses",
            fecha_limite=(date.today() + timedelta(days=30)).isoformat(),
            medio_postulacion="https://x.pe/a",
            email_contacto="rrhh@x.pe",
            no_discriminacion="on",
            regimen="728",
            salario_confidencial="",
        )
        datos.update(kw)
        return datos


class VerificacionTests(BaseEmpresaDash):
    def test_ca3__no_verificada_dashboard_limitado(self):
        """CA-3: empresa no verificada ve dashboard limitado y no puede publicar."""
        self._empresa_con_login(estado=EMP_PENDIENTE)
        resp = self.client.get(reverse("empresas:dashboard"))
        self.assertContains(resp, "verificación")
        # Y el form de publicar la rebota.
        resp2 = self.client.get(reverse("empresas:publicar"), follow=True)
        self.assertContains(resp2, "en verificación")

    def test_ca3__verificada_ve_metricas(self):
        empresa = self._empresa_con_login()
        resp = self.client.get(reverse("empresas:dashboard"))
        self.assertContains(resp, "Mis convocatorias")


class PublicarTests(BaseEmpresaDash):
    def test_ca2__publicar_crea_convocatoria(self):
        """CA-2: la empresa publica con el formulario (queda pendiente o auto-publicada)."""
        empresa = self._empresa_con_login()
        datos = self._datos_conv(carreras_objetivo=[self.sistemas.id])
        resp = self.client.post(reverse("empresas:publicar"), datos, follow=True)
        self.assertEqual(resp.status_code, 200)
        conv = Convocatoria.objects.get(titulo="Analista")
        self.assertEqual(conv.empresa, empresa)
        self.assertEqual(conv.creada_por, CREADA_POR_EMPRESA)
        # Empresa verificada pero transparencia media → revisión (pendiente).
        self.assertIn(conv.estado, [ESTADO_PENDIENTE, ESTADO_PUBLICADA])

    def test_ca2__auto_publica_si_verde(self):
        empresa = self._empresa_con_login(username="recl2")
        datos = self._datos_conv(
            carreras_objetivo=[self.sistemas.id],
            banda_salarial_min="2500", banda_salarial_max="3500",
            vacantes="3", beneficios="EPS, capacitación", discapacidad="on",
        )
        self.client.post(reverse("empresas:publicar"), datos)
        conv = Convocatoria.objects.get(titulo="Analista")
        self.assertEqual(conv.estado, ESTADO_PUBLICADA)  # verificada + 🟢 + sin alertas


class ObservadaTests(BaseEmpresaDash):
    def test_ca4__corregir_observada_vuelve_a_revision(self):
        """CA-4: una observada se corrige y vuelve a revisión (pendiente)."""
        empresa = self._empresa_con_login(username="recl3")
        conv = Convocatoria.objects.create(
            empresa=empresa, tipo=constants.TIPO_EMPLEO, titulo="Vieja",
            descripcion="x" * 120, modalidad="remoto", ubicacion="AQP",
            duracion_estimada="6m", fecha_limite=date.today() + timedelta(days=20),
            medio_postulacion="https://x.pe", email_contacto="a@x.pe",
            no_discriminacion=True, regimen="728", estado=ESTADO_OBSERVADA,
            comentario_revision="Agrega banda salarial.",
        )
        conv.carreras_objetivo.set([self.sistemas])
        datos = self._datos_conv(titulo="Vieja corregida", carreras_objetivo=[self.sistemas.id])
        self.client.post(reverse("empresas:editar", args=[conv.id]), datos)
        conv.refresh_from_db()
        self.assertEqual(conv.titulo, "Vieja corregida")
        self.assertIn(conv.estado, [ESTADO_PENDIENTE, ESTADO_PUBLICADA])

    def test_ca4__muestra_comentario(self):
        empresa = self._empresa_con_login(username="recl4")
        conv = Convocatoria.objects.create(
            empresa=empresa, tipo=constants.TIPO_EMPLEO, titulo="Obs",
            estado=ESTADO_OBSERVADA, comentario_revision="Corrige el sueldo.",
        )
        resp = self.client.get(reverse("empresas:editar", args=[conv.id]))
        self.assertContains(resp, "Corrige el sueldo.")


class MetricasTests(BaseEmpresaDash):
    def test_ca5__metricas_calculadas(self):
        """CA-5: métricas propias calculadas de datos reales."""
        from .services import metricas_empresa

        empresa = self._empresa_con_login(username="recl5")
        c = Convocatoria.objects.create(
            empresa=empresa, tipo=constants.TIPO_EMPLEO, titulo="Activa",
            estado=ESTADO_PUBLICADA, fecha_limite=date.today() + timedelta(days=10),
        )
        c.carreras_objetivo.set([self.sistemas])
        m = metricas_empresa(empresa)
        self.assertEqual(m["activas"], 1)
        self.assertEqual(m["publicadas"], 1)


import tempfile

from django.test import override_settings


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class EditarPerfilTests(BaseEmpresaDash):
    """Edición del perfil de empresa: cierra el ciclo de la completitud."""

    def _logo_png(self):
        """Genera un PNG mínimo válido para subir como logo."""
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image

        buf = BytesIO()
        Image.new("RGB", (10, 10), "red").save(buf, "PNG")
        return SimpleUploadedFile("logo.png", buf.getvalue(), content_type="image/png")

    def test_editar_perfil_sube_completitud(self):
        from .services import completitud_empresa

        empresa = self._empresa_con_login()
        self.assertEqual(self.client.get(reverse("empresas:editar_perfil")).status_code, 200)
        resp = self.client.post(
            reverse("empresas:editar_perfil"),
            {
                "razon_social": "ACME S.A.C.",
                "tipo": "sac",
                "telefono": "054-111222",
                "direccion": "Av. Siempre Viva 123",
                "web": "https://acme.pe",
                # El logo ahora se sube como imagen (ya no como URL).
                "logo_img": self._logo_png(),
                "descripcion": "Empresa de software con sede en Arequipa.",
            },
            follow=True,
        )
        self.assertRedirects(resp, reverse("empresas:dashboard"))
        empresa.refresh_from_db()
        self.assertEqual(empresa.descripcion, "Empresa de software con sede en Arequipa.")
        self.assertTrue(empresa.logo_img)  # la imagen quedó guardada
        self.assertEqual(completitud_empresa(empresa)["pct"], 100)
