"""Tests de la feature 04-convocatorias (criterios EARS)."""

from datetime import date, timedelta
from decimal import Decimal

from django.core.management import call_command
from django.test import TestCase

from apps.core import constants
from apps.empresas.models import ESTADO_ACTIVA, Empresa
from apps.taxonomia.models import Area
from apps.taxonomia.services import expandir

from .models import (
    CREADA_POR_ADMIN,
    ESTADO_PENDIENTE,
    MODALIDAD_REMOTO,
    Convocatoria,
)
from .services import (
    REGLAS_POR_TIPO,
    calcular_transparencia,
    campos_requeridos,
    publicar,
    validar_legal,
)


class BaseConvocatoria(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_config")
        call_command("seed_taxonomia")
        cls.empresa = Empresa.objects.create(
            ruc="20100000001", razon_social="Altiplano Tech SAC", estado=ESTADO_ACTIVA
        )

    def _conv(self, **kwargs):
        defaults = dict(
            empresa=self.empresa,
            tipo=constants.TIPO_EMPLEO,
            titulo="Desarrollador",
            descripcion="x" * 120,
            modalidad=MODALIDAD_REMOTO,
            ubicacion="Arequipa",
            duracion_estimada="6 meses",
            fecha_limite=date.today() + timedelta(days=30),
            medio_postulacion="https://acme.pe/postular",
            email_contacto="rrhh@acme.pe",
            no_discriminacion=True,
            regimen="D.L. 728",
        )
        defaults.update(kwargs)
        return Convocatoria.objects.create(**defaults)


class TiposTests(BaseConvocatoria):
    def test_ca1__ocho_tipos(self):
        """CA-1: existen 8 tipos de convocatoria soportados."""
        self.assertEqual(len(constants.TIPOS_CONVOCATORIA), 8)
        self.assertEqual(len(REGLAS_POR_TIPO), 8)

    def test_ca3__campos_requeridos_por_tipo(self):
        """CA-3: cada tipo exige sus campos Nivel 2 (convenio en preprof, régimen en empleo)."""
        self.assertIn(
            "requiere_convenio", campos_requeridos(constants.TIPO_PRACTICA_PREPROFESIONAL)
        )
        self.assertIn("regimen", campos_requeridos(constants.TIPO_EMPLEO))

    def test_ca3__falta_campo_nivel2_es_error(self):
        conv = self._conv(tipo=constants.TIPO_PRACTICA_PREPROFESIONAL, regimen="")
        errores = validar_legal(conv)
        self.assertTrue(any("convenio" in e.lower() for e in errores))


class ValidacionLegalTests(BaseConvocatoria):
    def test_ca4__subvencion_menor_a_rmv_bloquea(self):
        """CA-4: una remuneración menor a la RMV produce error."""
        conv = self._conv(tipo=constants.TIPO_EMPLEO, subvencion_remuneracion=Decimal("500"))
        errores = validar_legal(conv)
        self.assertTrue(any("RMV" in e for e in errores))

    def test_ca4__subvencion_igual_o_mayor_rmv_ok(self):
        conv = self._conv(tipo=constants.TIPO_EMPLEO, subvencion_remuneracion=Decimal("1500"))
        self.assertEqual(validar_legal(conv), [])

    def test_ca5__voluntariado_sin_remuneracion(self):
        """CA-5: el voluntariado no admite remuneración."""
        conv = self._conv(
            tipo=constants.TIPO_VOLUNTARIADO,
            subvencion_remuneracion=Decimal("800"),
            regimen="",
        )
        errores = validar_legal(conv)
        self.assertTrue(any("voluntariado" in e.lower() for e in errores))

    def test_ca5__voluntariado_sin_pago_es_valido(self):
        conv = self._conv(
            tipo=constants.TIPO_VOLUNTARIADO, subvencion_remuneracion=None, regimen=""
        )
        self.assertEqual(validar_legal(conv), [])

    def test__jornada_excede_tope_preprofesional(self):
        conv = self._conv(
            tipo=constants.TIPO_PRACTICA_PREPROFESIONAL,
            requiere_convenio=True,
            ciclo_minimo=6,
            jornada_horas=40,  # tope 30
        )
        errores = validar_legal(conv)
        self.assertTrue(any("jornada" in e.lower() for e in errores))


class TransparenciaTests(BaseConvocatoria):
    def test_ca6__sueldo_pesa_30(self):
        """CA-6: la banda salarial visible aporta 30% del total."""
        base = self._conv(titulo="Sin sueldo", descripcion="x" * 120)
        sin = calcular_transparencia(base)
        base.banda_salarial_min = Decimal("2000")
        base.banda_salarial_max = Decimal("3000")
        con = calcular_transparencia(base)
        self.assertEqual(con - sin, 30)

    def test_ca6__confidencial_no_suma_banda(self):
        conv = self._conv(
            banda_salarial_min=Decimal("2000"),
            banda_salarial_max=Decimal("3000"),
            salario_confidencial=True,
        )
        sin = calcular_transparencia(self._conv(titulo="otra"))
        self.assertEqual(calcular_transparencia(conv), sin)

    def test_ca7__etiqueta_semaforo(self):
        """CA-7: etiqueta 🟢≥80 / 🟡50–79 / 🔴<50."""
        conv = self._conv(
            banda_salarial_min=Decimal("2000"), banda_salarial_max=Decimal("3000"),
            vacantes=3, beneficios="EPS, movilidad", discapacidad=True,
        )
        conv.recalcular_transparencia()
        self.assertGreaterEqual(conv.transparencia_pct, 80)
        self.assertEqual(conv.etiqueta_transparencia, "alta")

        pobre = self._conv(
            titulo="pobre", descripcion="corto", duracion_estimada="",
            modalidad="", ubicacion="", email_contacto="", medio_postulacion="",
        )
        pobre.recalcular_transparencia()
        self.assertLess(pobre.transparencia_pct, 50)
        self.assertEqual(pobre.etiqueta_transparencia, "baja")


class PublicacionTests(BaseConvocatoria):
    def test_ca2__nivel1_completo_permite_publicar(self):
        """CA-2: con Nivel 1 completo, publicar deja la convocatoria en pendiente."""
        conv = self._conv()
        errores = publicar(conv)
        self.assertEqual(errores, [])
        conv.refresh_from_db()
        self.assertEqual(conv.estado, ESTADO_PENDIENTE)
        self.assertGreater(conv.transparencia_pct, 0)

    def test_ca2__nivel1_incompleto_no_publica(self):
        conv = self._conv(titulo="x", descripcion="", ubicacion="", duracion_estimada="")
        errores = publicar(conv)
        self.assertTrue(errores)

    def test_ca10__sin_no_discriminacion_no_publica(self):
        """CA-10: publicar exige el checkbox de no discriminación."""
        conv = self._conv(no_discriminacion=False)
        errores = publicar(conv)
        self.assertTrue(any("discriminación" in e.lower() for e in errores))


class TargetingTests(BaseConvocatoria):
    def test_ca8__carreras_objetivo_via_expandir(self):
        """CA-8: la convocatoria se asocia a carreras objetivo (expansión de taxonomía)."""
        conv = self._conv()
        area = Area.objects.get(nombre="Biomédicas")
        conv.carreras_objetivo.set(expandir(area))
        self.assertEqual(conv.carreras_objetivo.count(), 6)


class OrigenTests(BaseConvocatoria):
    def test_ca9__creada_por_admin_y_empresa_referencial(self):
        """CA-9: registra creada_por y soporta empresa referencial."""
        referencial = Empresa.objects.create(
            ruc="20100000999", razon_social="Referencial SAC", estado=ESTADO_ACTIVA
        )
        conv = self._conv(empresa=referencial, creada_por=CREADA_POR_ADMIN)
        self.assertEqual(conv.creada_por, CREADA_POR_ADMIN)
        self.assertTrue(referencial.es_referencial)
        self.assertEqual(referencial.convocatorias.count(), 1)
