"""Tests de la feature 03-empresas (criterios EARS)."""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from apps.usuarios.models import ROL_RECLUTADOR

from .models import ESTADO_ACTIVA, ESTADO_PENDIENTE, Empresa, Reclutador
from .services import activar_empresa, empresa_puede_publicar

User = get_user_model()


def _datos_registro(ruc="20123456789", username="empresa_acme"):
    return {
        # Bloque A
        "ruc": ruc,
        "razon_social": "ACME S.A.C.",
        "nombre_comercial": "ACME",
        "tipo": "sac",
        "ciiu": "6201",
        "telefono": "054-123456",
        "direccion": "Av. Siempre Viva 123",
        "web": "",
        "linkedin": "",
        "logo_url": "",
        "banner_url": "",
        "video_url": "",
        "descripcion": "Software.",
        # Bloque B
        "dni": "12345678",
        "nombres": "Juan",
        "ap_paterno": "Pérez",
        "ap_materno": "Gómez",
        "cargo": "RR.HH.",
        "email": "juan@acme.pe",
        "telefono": "987654321",
        "username": username,
        "password1": "claveSegura123",
        "password2": "claveSegura123",
    }


class EmpresaInvariantesTests(TestCase):
    def test_entidad_valida_pasa_full_clean(self):
        empresa = Empresa(ruc="20123456789", razon_social="ACME S.A.C.")

        empresa.full_clean()

        self.assertEqual(empresa.ruc, "20123456789")
        self.assertEqual(empresa.razon_social, "ACME S.A.C.")

    def test_ruc_con_longitud_distinta_de_11_falla(self):
        empresa = Empresa(ruc="1234567890", razon_social="ACME S.A.C.")

        with self.assertRaises(ValidationError):
            empresa.full_clean()

    def test_razon_social_vacia_falla(self):
        empresa = Empresa(ruc="20123456789", razon_social="")

        with self.assertRaises(ValidationError):
            empresa.full_clean()


class SeedCuentasRefactorTests(TestCase):
    def test_seed_cuentas_exige_password_de_entorno(self):
        from apps.empresas.management.commands import seed_cuentas

        with patch.object(seed_cuentas, "PASSWORD_DEMO", ""):
            with self.assertRaises(CommandError):
                call_command("seed_cuentas")

    def test_seed_cuentas_crea_reclutador_demo(self):
        from apps.empresas.management.commands import seed_cuentas

        empresa = Empresa.objects.create(
            ruc="20100000011",
            razon_social="Globant Perú S.A.C.",
            nombre_comercial="Globant",
        )
        with patch.object(seed_cuentas, "PASSWORD_DEMO", "clave-demo"):
            call_command("seed_cuentas")

        empresa.refresh_from_db()
        self.assertEqual(empresa.reclutador.usuario.email, "talento@globant.com")


class SeedImagenesRefactorTests(TestCase):
    def test_mime_png_y_jpeg(self):
        from apps.empresas.management.commands.seed_imagenes import _mime

        self.assertEqual(_mime(b"\x89PNG\r\n\x1a\n" + b"0" * 24), "image/png")
        self.assertEqual(_mime(b"\xff\xd8\xff" + b"0" * 24), "image/jpeg")

    def test_tarjeta_svg_contiene_logo(self):
        from apps.empresas.management.commands.seed_imagenes import _tarjeta_svg

        svg = _tarjeta_svg(b"\x89PNG\r\n\x1a\n" + b"0" * 24)
        self.assertIn("<svg", svg)
        self.assertIn("data:image/png;base64,", svg)

    def test_resumen_transparencia_sin_convocatorias(self):
        from apps.empresas.views import _resumen_transparencia

        self.assertIsNone(_resumen_transparencia([], 0, {}))

    def test_resumen_atencion_separa_observadas_y_por_vencer(self):
        from datetime import timedelta
        from apps.empresas.views import _resumen_atencion

        class Conv:
            estado = ESTADO_PENDIENTE
            dias_restantes = None

        observada = Conv()
        observada.estado = "observada"
        por_vencer = Conv()
        por_vencer.estado = "publicada"
        por_vencer.dias_restantes = 3

        resumen = _resumen_atencion([observada, por_vencer])
        self.assertEqual(resumen["observadas"], 1)
        self.assertEqual(resumen["por_vencer"], 1)

    def test_dims_png_y_svg(self):
        from apps.empresas.management.commands.seed_imagenes import _dims

        png = (
            b"\x89PNG\r\n\x1a\n"
            + b"\x00" * 8
            + (128).to_bytes(4, "big")
            + (64).to_bytes(4, "big")
        )
        self.assertEqual(_dims(png), (128, 64))
        self.assertEqual(_dims(b"<svg viewBox='0 0 512 512'>"), (512, 512))
        self.assertEqual(_dims(b"\x00\x00\x01\x00"), (0, 0))
        self.assertEqual(_dims(b"<svg viewBox='0 0 512 512'>")[0], 512)


class RegistroEmpresaTests(TestCase):
    def test_registro_rechaza_metodos_distintos(self):
        resp = self.client.put(reverse("empresas:registro"))
        self.assertEqual(resp.status_code, 405)

    def test_ca1__registro_crea_empresa_pendiente(self):
        """CA-1: el registro crea la empresa en estado pendiente."""
        resp = self.client.post(reverse("empresas:registro"), _datos_registro())
        self.assertRedirects(resp, reverse("empresas:registro_exito"))
        empresa = Empresa.objects.get(ruc="20123456789")
        self.assertEqual(empresa.estado, ESTADO_PENDIENTE)
        self.assertEqual(empresa.reclutador.nombres, "Juan")
        self.assertEqual(empresa.reclutador.usuario.perfil.rol, ROL_RECLUTADOR)

    def test_ca7__ruc_duplicado_rechazado(self):
        """CA-7: un RUC ya existente impide el registro duplicado."""
        self.client.post(reverse("empresas:registro"), _datos_registro())
        resp = self.client.post(
            reverse("empresas:registro"), _datos_registro(username="otro_user")
        )
        self.assertEqual(resp.status_code, 200)  # vuelve al form con error
        self.assertContains(resp, "Ya existe Empresa con este RUC.", status_code=200)
        self.assertEqual(Empresa.objects.filter(ruc="20123456789").count(), 1)

    def test__username_duplicado_rechazado(self):
        self.client.post(reverse("empresas:registro"), _datos_registro())
        resp = self.client.post(
            reverse("empresas:registro"),
            _datos_registro(ruc="20999999999"),  # mismo username
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Ese usuario ya está en uso.")


class EstadoEmpresaTests(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(ruc="20111111111", razon_social="Beta SAC")
        self.user = User.objects.create_user("beta_user", password="x")
        Reclutador.objects.create(
            usuario=self.user, empresa=self.empresa, nombres="Ana", ap_paterno="Lopez"
        )

    def test_ca2__pendiente_no_puede_publicar(self):
        """CA-2: mientras esté pendiente, no puede publicar."""
        self.assertEqual(self.empresa.estado, ESTADO_PENDIENTE)
        self.assertFalse(empresa_puede_publicar(self.empresa))
        self.assertFalse(self.empresa.puede_publicar)

    def test_ca3__activar_permite_publicar_y_verifica(self):
        """CA-3: al activar, puede publicar y muestra badge Verificada."""
        activar_empresa(self.empresa)
        self.empresa.refresh_from_db()
        self.assertEqual(self.empresa.estado, ESTADO_ACTIVA)
        self.assertTrue(empresa_puede_publicar(self.empresa))
        self.assertTrue(self.empresa.verificada)

    def test_ca5__un_reclutador_por_empresa(self):
        """CA-5: la empresa admite un único reclutador (OneToOne)."""
        otro = User.objects.create_user("otro", password="x")
        from django.db import IntegrityError, transaction

        with self.assertRaises(IntegrityError), transaction.atomic():
            Reclutador.objects.create(
                usuario=otro, empresa=self.empresa, nombres="Luis", ap_paterno="Diaz"
            )


class EmpresaReferencialTests(TestCase):
    def test_ca4__referencial_sin_badge(self):
        """CA-4: una empresa referencial (sin reclutador) no muestra badge aunque esté activa."""
        ref = Empresa.objects.create(
            ruc="20222222222", razon_social="Referencial SAC", estado=ESTADO_ACTIVA
        )
        self.assertTrue(ref.es_referencial)
        self.assertFalse(ref.verificada)
        # Pero el admin sí puede asociarle convocatorias (puede_publicar = activa).
        self.assertTrue(ref.puede_publicar)

    def test_ca6__logo_y_banner_son_url(self):
        """CA-6: logo y banner se guardan como URL."""
        empresa = Empresa.objects.create(
            ruc="20333333333",
            razon_social="Gamma",
            logo_url="https://cdn.example.com/logo.png",
            banner_url="https://cdn.example.com/banner.png",
        )
        self.assertTrue(empresa.logo_url.startswith("https://"))
        self.assertTrue(empresa.banner_url.startswith("https://"))
