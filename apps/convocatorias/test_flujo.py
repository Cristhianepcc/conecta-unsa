"""Tests de la feature 06-flujo-admin (criterios EARS)."""

from datetime import date, timedelta
from decimal import Decimal

from django.core.management import call_command
from django.test import TestCase

from apps.core import constants
from apps.empresas.models import ESTADO_ACTIVA, Empresa, Reclutador
from django.contrib.auth import get_user_model

from . import flujo
from .models import (
    CREADA_POR_ADMIN,
    ESTADO_CADUCADA,
    ESTADO_OBSERVADA,
    ESTADO_PENDIENTE,
    ESTADO_PUBLICADA,
    MODALIDAD_REMOTO,
    Convocatoria,
)

User = get_user_model()


class BaseFlujo(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_config")

    def _empresa(self, ruc="20600000001", verificada=True, referencial=False):
        empresa = Empresa.objects.create(
            ruc=ruc, razon_social="Empresa Flujo", estado=ESTADO_ACTIVA
        )
        if verificada and not referencial:
            user = User.objects.create_user(f"rec{ruc}", password="x")
            Reclutador.objects.create(
                usuario=user, empresa=empresa, nombres="R", ap_paterno="X"
            )
        return empresa

    def _conv(self, empresa, **kwargs):
        defaults = dict(
            empresa=empresa,
            tipo=constants.TIPO_EMPLEO,
            titulo="Analista de datos",
            descripcion="x" * 120,
            modalidad=MODALIDAD_REMOTO,
            ubicacion="Arequipa",
            duracion_estimada="6 meses",
            fecha_limite=date.today() + timedelta(days=30),
            medio_postulacion="https://x.pe",
            email_contacto="rrhh@x.pe",
            no_discriminacion=True,
            regimen="728",
        )
        defaults.update(kwargs)
        conv = Convocatoria.objects.create(**defaults)
        conv.recalcular_transparencia()
        return conv

    def _conv_verde(self, empresa, **kwargs):
        """Convocatoria con alta transparencia (🟢)."""
        kwargs.setdefault("banda_salarial_min", Decimal("2500"))
        kwargs.setdefault("banda_salarial_max", Decimal("3500"))
        kwargs.setdefault("vacantes", 3)
        kwargs.setdefault("beneficios", "EPS, capacitación, movilidad")
        kwargs.setdefault("discapacidad", True)
        return self._conv(empresa, **kwargs)


class EstadosTests(BaseFlujo):
    def test_ca1__transiciones_validas(self):
        conv = self._conv(self._empresa(), estado=ESTADO_PENDIENTE)
        flujo.mover_estado(conv, ESTADO_PUBLICADA)
        self.assertEqual(conv.estado, ESTADO_PUBLICADA)

    def test_ca1__transicion_invalida_lanza(self):
        conv = self._conv(self._empresa(), estado=ESTADO_PUBLICADA)
        with self.assertRaises(flujo.TransicionInvalida):
            flujo.mover_estado(conv, ESTADO_PENDIENTE)

    def test__activa_property(self):
        conv = self._conv(self._empresa(), estado=ESTADO_PUBLICADA)
        self.assertTrue(conv.activa)
        conv.fecha_limite = date.today() - timedelta(days=1)
        self.assertFalse(conv.activa)


class AlertasTests(BaseFlujo):
    def test_ca2__alerta_baja_transparencia(self):
        empresa = self._empresa()
        conv = self._conv(empresa, descripcion="corto", duracion_estimada="",
                          modalidad="", ubicacion="")
        self.assertIn(flujo.ALERTA_BAJA_TRANSPARENCIA, flujo.calcular_alertas(conv))

    def test_ca2__alerta_incompleta(self):
        conv = self._conv(self._empresa(), titulo="x", no_discriminacion=False,
                          descripcion="", ubicacion="", duracion_estimada="")
        self.assertIn(flujo.ALERTA_INCOMPLETA, flujo.calcular_alertas(conv))

    def test_ca3__duplicado_misma_empresa_titulo_similar(self):
        """CA-3: misma empresa + título similar + ≤30 días → alerta duplicado."""
        empresa = self._empresa()
        self._conv_verde(empresa, titulo="Analista de Datos Senior")
        nueva = self._conv_verde(empresa, titulo="Analista de datos senior")
        dups = flujo.detectar_duplicado(nueva)
        self.assertTrue(dups)
        self.assertIn(flujo.ALERTA_DUPLICADO, flujo.calcular_alertas(nueva))

    def test_ca3__titulos_distintos_no_duplican(self):
        empresa = self._empresa()
        self._conv_verde(empresa, titulo="Contador público")
        nueva = self._conv_verde(empresa, titulo="Chef ejecutivo de cocina")
        self.assertEqual(flujo.detectar_duplicado(nueva), [])


class SemaforoTests(BaseFlujo):
    def test_ca4__verificada_verde_sin_alertas_auto(self):
        """CA-4: empresa verificada + 🟢 + sin alertas → auto-publica."""
        empresa = self._empresa(verificada=True)
        conv = self._conv_verde(empresa)
        self.assertEqual(conv.etiqueta_transparencia, "alta")
        self.assertEqual(flujo.decidir_publicacion(conv), "auto")
        destino = flujo.procesar_envio(conv)
        self.assertEqual(destino, "auto")
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_PUBLICADA)
        self.assertIsNotNone(conv.fecha_publicacion)

    def test_ca5__empresa_referencial_va_a_revision(self):
        """CA-5: empresa no verificada → revisión humana (pendiente)."""
        empresa = self._empresa(ruc="20600000777", referencial=True)
        conv = self._conv_verde(empresa, creada_por=CREADA_POR_ADMIN)
        self.assertFalse(empresa.verificada)
        self.assertEqual(flujo.decidir_publicacion(conv), "revision")
        destino = flujo.procesar_envio(conv)
        self.assertEqual(destino, "revision")
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_PENDIENTE)

    def test_ca5__verificada_con_alertas_va_a_revision(self):
        empresa = self._empresa(ruc="20600000888")
        conv = self._conv(empresa, descripcion="corto", duracion_estimada="")  # baja transparencia
        self.assertEqual(flujo.decidir_publicacion(conv), "revision")


class AccionesAdminTests(BaseFlujo):
    def test_ca6__observar_registra_comentario(self):
        """CA-6: observar registra el comentario de revisión."""
        conv = self._conv(self._empresa(), estado=ESTADO_PENDIENTE)
        flujo.observar(conv, "Falta especificar la banda salarial.")
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_OBSERVADA)
        self.assertEqual(conv.comentario_revision, "Falta especificar la banda salarial.")

    def test__aprobar_publica(self):
        conv = self._conv(self._empresa(), estado=ESTADO_PENDIENTE)
        flujo.aprobar(conv)
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_PUBLICADA)


class CaducidadTests(BaseFlujo):
    def test_ca7__caduca_vencidas(self):
        """CA-7: una convocatoria publicada vencida pasa a caducada."""
        empresa = self._empresa()
        vigente = self._conv(empresa, estado=ESTADO_PUBLICADA,
                            fecha_limite=date.today() + timedelta(days=5))
        vencida = self._conv(empresa, titulo="Vieja", estado=ESTADO_PUBLICADA,
                           fecha_limite=date.today() - timedelta(days=1))
        n = flujo.caducar_vencidas()
        self.assertEqual(n, 1)
        vencida.refresh_from_db()
        vigente.refresh_from_db()
        self.assertEqual(vencida.estado, ESTADO_CADUCADA)
        self.assertEqual(vigente.estado, ESTADO_PUBLICADA)
