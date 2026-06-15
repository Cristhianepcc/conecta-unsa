"""Tests de la feature 05-matching (criterios EARS)."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.core import constants
from apps.convocatorias.models import ESTADO_PUBLICADA, Convocatoria
from apps.empresas.models import ESTADO_ACTIVA, Empresa
from apps.taxonomia.models import Carrera
from apps.usuarios.models import (
    FUENTE_VERIFICADO,
    Credencial,
    PerfilTalento,
)
from apps.notificaciones.services import construir_resumen

from . import services

User = get_user_model()


class BaseMatching(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_config")
        call_command("seed_taxonomia")
        call_command("seed_elegibilidad")
        cls.empresa = Empresa.objects.create(
            ruc="20500000001", razon_social="Altiplano Tech", estado=ESTADO_ACTIVA
        )
        cls.sistemas = Carrera.objects.get(nombre="Ingeniería de Sistemas")
        cls.medicina = Carrera.objects.get(nombre="Medicina")

    def _conv(self, tipo, carreras, **kwargs):
        conv = Convocatoria.objects.create(
            empresa=self.empresa, tipo=tipo, titulo=kwargs.pop("titulo", "Conv"),
            estado=ESTADO_PUBLICADA, **kwargs,
        )
        conv.carreras_objetivo.set(carreras)
        return conv

    def _egresado(self, carrera, estado="egresado", username="u"):
        user = User.objects.create_user(username, email=f"{username}@gmail.com", password="x")
        talento, _ = PerfilTalento.objects.get_or_create(usuario=user)
        talento.carrera = carrera
        talento.estado_academico = estado
        talento.save()
        return user


class Gate1Tests(BaseMatching):
    def test_ca1__estudiante_no_ve_empleo(self):
        """CA-1: un estudiante no es elegible para 'empleo'."""
        self._conv(constants.TIPO_EMPLEO, [self.sistemas], titulo="Empleo")
        user = self._egresado(self.sistemas, estado="estudiante", username="est")
        qs = services.elegibles_por_estado(user)
        self.assertEqual(qs.count(), 0)

    def test_ca1__egresado_no_ve_preprofesional(self):
        """CA-1: un egresado no es elegible para 'práctica preprofesional'."""
        self._conv(constants.TIPO_PRACTICA_PREPROFESIONAL, [self.sistemas], titulo="Preprof")
        user = self._egresado(self.sistemas, estado="egresado", username="egr")
        qs = services.elegibles_por_estado(user)
        self.assertEqual(qs.count(), 0)

    def test_ca1__egresado_si_ve_empleo(self):
        self._conv(constants.TIPO_EMPLEO, [self.sistemas], titulo="Empleo")
        user = self._egresado(self.sistemas, estado="egresado", username="egr2")
        self.assertEqual(services.elegibles_por_estado(user).count(), 1)

    def test_ca7__matriz_desde_bd(self):
        """CA-7: la elegibilidad sale de ReglaElegibilidad (config-as-data)."""
        self.assertIn(constants.TIPO_PRACTICA_PREPROFESIONAL,
                      services.tipos_elegibles("estudiante"))
        self.assertNotIn(constants.TIPO_EMPLEO, services.tipos_elegibles("estudiante"))


class Gate2Tests(BaseMatching):
    def test_ca2__solo_convocatorias_de_su_carrera(self):
        """CA-2: excluye convocatorias cuyas carreras objetivo no incluyen la del usuario."""
        self._conv(constants.TIPO_EMPLEO, [self.sistemas], titulo="Para Sistemas")
        self._conv(constants.TIPO_EMPLEO, [self.medicina], titulo="Para Medicina")
        user = self._egresado(self.sistemas, username="sis")
        qs = services.elegibles_por_carrera(user)
        titulos = set(qs.values_list("titulo", flat=True))
        self.assertEqual(titulos, {"Para Sistemas"})

    def test_ca2__carreras_extra_amplian_feed(self):
        self._conv(constants.TIPO_EMPLEO, [self.medicina], titulo="Para Medicina")
        user = self._egresado(self.sistemas, username="sis2")
        user.perfil_talento.carreras_extra.add(self.medicina)
        qs = services.elegibles_por_carrera(user)
        self.assertEqual(qs.count(), 1)


class Layer3Tests(BaseMatching):
    def test_ca3_ca4__ordena_por_afinidad_con_motivo(self):
        """CA-3/CA-4: lo más afín al perfil aparece primero, con motivo explicable."""
        trainee = self._conv(constants.TIPO_TRAINEE, [self.sistemas], titulo="Trainee")
        empleo = self._conv(constants.TIPO_EMPLEO, [self.sistemas], titulo="Empleo")
        user = self._egresado(self.sistemas, username="lider")
        Credencial.objects.create(
            perfil=user.perfil_talento, tipo="representacion", detalle="Delegado 2024"
        )
        feed = services.feed(user)
        primero, puntaje, motivos = feed[0]
        self.assertEqual(primero, trainee)  # representación potencia trainee
        self.assertGreater(puntaje, 0)
        self.assertTrue(any("Delegado" in m for m in motivos))

    def test_ca4__credencial_verificada_pesa_mas(self):
        conv = self._conv(constants.TIPO_BECA, [self.sistemas], titulo="Beca")
        user = self._egresado(self.sistemas, username="inv")
        Credencial.objects.create(
            perfil=user.perfil_talento, tipo="tesis", detalle="Tesis", fuente=FUENTE_VERIFICADO
        )
        _, puntaje, _ = services.rankear(user, Convocatoria.objects.filter(pk=conv.pk))[0]
        self.assertEqual(puntaje, services.PESO_CREDENCIAL_VERIFICADA)


class FeedSinPerfilTests(BaseMatching):
    def test_ca5__feed_funciona_sin_perfil_completo(self):
        """CA-5: el feed se muestra aunque el perfil esté incompleto (sin ranking duro)."""
        self._conv(constants.TIPO_EMPLEO, [self.sistemas], titulo="Empleo")
        user = User.objects.create_user("vacio", email="vacio@gmail.com", password="x")
        # Sin PerfilTalento con carrera/estado → no crashea y devuelve el feed.
        feed = services.feed(user)
        self.assertEqual(len(feed), 1)


class AlcanceTests(BaseMatching):
    def test_ca6__alcance_cuenta_egresados_que_califican(self):
        """CA-6: alcance = conteo de egresados cuya carrera y estado califican."""
        conv = self._conv(constants.TIPO_EMPLEO, [self.sistemas], titulo="Empleo")
        self._egresado(self.sistemas, estado="egresado", username="a1")
        self._egresado(self.sistemas, estado="titulado", username="a2")
        self._egresado(self.sistemas, estado="estudiante", username="a3")  # no califica empleo
        self._egresado(self.medicina, estado="egresado", username="a4")    # otra carrera
        self.assertEqual(services.alcance(conv), 2)


class VigenciaFeedTests(BaseMatching):
    """Feature 13: vencidas fuera del feed y del resumen, aunque el cron no haya corrido."""

    def test_ca1__vencida_no_aparece_en_feed(self):
        """CA-1: una publicada con fecha límite pasada no entra al feed."""
        vigente = self._conv(
            constants.TIPO_EMPLEO, [self.sistemas], titulo="Vigente",
            fecha_limite=date.today() + timedelta(days=10),
        )
        vencida = self._conv(
            constants.TIPO_EMPLEO, [self.sistemas], titulo="Vencida",
            fecha_limite=date.today() - timedelta(days=1),
        )
        user = self._egresado(self.sistemas, username="vig")
        ids = [c.id for c, _p, _m in services.feed(user)]
        self.assertIn(vigente.id, ids)
        self.assertNotIn(vencida.id, ids)

    def test_ca2__resumen_excluye_vencida(self):
        """CA-2: el resumen semanal hereda el filtro de vigencia (vía matching.feed)."""
        vigente = self._conv(
            constants.TIPO_EMPLEO, [self.sistemas], titulo="Vigente",
            fecha_limite=date.today() + timedelta(days=10),
        )
        vencida = self._conv(
            constants.TIPO_EMPLEO, [self.sistemas], titulo="Vencida",
            fecha_limite=date.today() - timedelta(days=1),
        )
        user = self._egresado(self.sistemas, username="res")
        ids = [c.id for c in construir_resumen(user)]
        self.assertIn(vigente.id, ids)
        self.assertNotIn(vencida.id, ids)

    def test_ca3__sin_fecha_limite_no_expira(self):
        """CA-3: una convocatoria sin fecha límite (null) sigue apareciendo."""
        sin_fecha = self._conv(
            constants.TIPO_EMPLEO, [self.sistemas], titulo="Sin fecha", fecha_limite=None
        )
        user = self._egresado(self.sistemas, username="nofecha")
        ids = [c.id for c, _p, _m in services.feed(user)]
        self.assertIn(sin_fecha.id, ids)

    def test__publicadas_solo_vigentes(self):
        """convocatorias_publicadas() excluye las vencidas en el origen."""
        self._conv(
            constants.TIPO_EMPLEO, [self.sistemas], titulo="Vencida",
            fecha_limite=date.today() - timedelta(days=1),
        )
        self.assertEqual(services.convocatorias_publicadas().count(), 0)
