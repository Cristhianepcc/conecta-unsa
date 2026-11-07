"""Issue #2 - Pruebas unitarias de Dominio (Servicios): apps/matching/services.py

Pruebas unitarias puras (sin BD) con dobles de prueba: SimpleNamespace / MagicMock / patch.
Las que necesitan la BD están marcadas con @pytest.mark.django_db.
"""

from datetime import date, timedelta
from types import SimpleNamespace as NS
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from apps.core import constants
from apps.convocatorias.models import (
    ESTADO_OBSERVADA, ESTADO_PENDIENTE, ESTADO_PUBLICADA, Convocatoria,
)
from apps.empresas.models import ESTADO_ACTIVA, Empresa
from apps.matching import services
from apps.taxonomia.models import Carrera
from apps.usuarios.models import FUENTE_VERIFICADO, Credencial, PerfilTalento

User = get_user_model()


# --------------------------------------------------------------------------- dobles
def cred(tipo, verificada=False, detalle=""):
    return NS(tipo=tipo, verificada=verificada, detalle=detalle,
              get_tipo_display=lambda: f"display-{tipo}")


def usuario(carrera_id=None, carrera="Sistemas", creds=(), preferidos=(), estado="egresado",
            silenciadas=()):
    credenciales = MagicMock()
    credenciales.all.return_value = list(creds)
    perfil = MagicMock()
    perfil.carrera_id = carrera_id
    perfil.carrera = carrera
    perfil.credenciales = credenciales
    perfil.tipos_preferidos = list(preferidos)
    perfil.estado_academico = estado
    perfil.categorias_silenciadas = list(silenciadas)
    return NS(perfil_talento=perfil)


def conv(tipo=constants.TIPO_EMPLEO, en_carrera=True, **kw):
    carreras = MagicMock()
    carreras.filter.return_value.exists.return_value = en_carrera
    return NS(tipo=tipo, carreras_objetivo=carreras, **kw)


# -------------------------------------------------------------------- compatibilidad
class TestCompatibilidad:
    def test_usuario_sin_perfil_da_55_sin_chips(self):
        assert services.compatibilidad(NS(), conv()) == (55, [])

    def test_carrera_propia_en_objetivo_suma_15_y_chip(self):
        pct, chips = services.compatibilidad(usuario(carrera_id=1, carrera="Sistemas"), conv())
        assert pct == 70
        assert chips == ["Sistemas"]

    def test_carrera_afin_suma_solo_6(self):
        pct, chips = services.compatibilidad(usuario(carrera_id=1), conv(en_carrera=False))
        assert pct == 61
        assert chips == []

    def test_perfil_sin_carrera_no_suma_bonus_de_carrera(self):
        pct, _ = services.compatibilidad(usuario(carrera_id=None), conv())
        assert pct == 55

    def test_credencial_verificada_suma_8(self):
        u = usuario(creds=[cred("idioma", verificada=True)])
        assert services.compatibilidad(u, conv()) == (63, ["Idioma"])

    def test_credencial_autodeclarada_suma_6(self):
        u = usuario(creds=[cred("idioma", verificada=False)])
        assert services.compatibilidad(u, conv()) == (61, ["Idioma"])

    def test_credencial_no_relevante_para_el_tipo_no_suma(self):
        u = usuario(creds=[cred("tesis")])  # tesis potencia becas, no empleo
        assert services.compatibilidad(u, conv(constants.TIPO_EMPLEO)) == (55, [])

    def test_chip_no_se_duplica_con_dos_credenciales_iguales(self):
        u = usuario(creds=[cred("idioma"), cred("idioma")])
        pct, chips = services.compatibilidad(u, conv())
        assert chips == ["Idioma"]
        assert pct == 67  # ambas suman

    def test_tipo_preferido_suma_8_y_chip(self):
        u = usuario(preferidos=[constants.TIPO_EMPLEO])
        assert services.compatibilidad(u, conv()) == (63, ["Tipo preferido"])

    def test_puntaje_tiene_tope_100(self):
        u = usuario(creds=[cred("idioma", verificada=True) for _ in range(10)])
        assert services.compatibilidad(u, conv())[0] == 100


# ------------------------------------------------------------------------- puntuar
class TestPuntuar:
    def test_sin_perfil_da_cero(self):
        assert services.puntuar(NS(), conv()) == (0, [])

    def test_credencial_verificada_pesa_15(self):
        u = usuario(creds=[cred("idioma", verificada=True, detalle="Inglés B2")])
        assert services.puntuar(u, conv()) == (services.PESO_CREDENCIAL_VERIFICADA, ["Inglés B2"])

    def test_credencial_autodeclarada_pesa_10(self):
        u = usuario(creds=[cred("idioma", verificada=False, detalle="Inglés B1")])
        assert services.puntuar(u, conv())[0] == services.PESO_CREDENCIAL

    def test_motivo_usa_display_si_no_hay_detalle(self):
        u = usuario(creds=[cred("idioma", detalle="")])
        assert services.puntuar(u, conv())[1] == ["display-idioma"]

    def test_credencial_que_no_potencia_el_tipo_no_suma(self):
        u = usuario(creds=[cred("tesis")])
        assert services.puntuar(u, conv(constants.TIPO_EMPLEO)) == (0, [])

    def test_tipo_preferido_suma_12_con_motivo(self):
        u = usuario(preferidos=[constants.TIPO_EMPLEO])
        assert services.puntuar(u, conv()) == (services.PESO_TIPO_PREFERIDO, ["tipo que prefieres"])

    def test_suma_credencial_y_tipo_preferido(self):
        u = usuario(creds=[cred("idioma", verificada=True, detalle="B2")],
                    preferidos=[constants.TIPO_EMPLEO])
        puntaje, motivos = services.puntuar(u, conv())
        assert puntaje == 15 + 12
        assert motivos == ["B2", "tipo que prefieres"]


# ------------------------------------------------------- gates y helpers sin BD
class TestGatesSinBD:
    def test_tipos_elegibles_estado_vacio_devuelve_set_vacio(self):
        assert services.tipos_elegibles("") == set()

    def test_elegibles_por_estado_sin_perfil_no_filtra(self):
        qs = MagicMock()
        assert services.elegibles_por_estado(NS(), qs) is qs

    def test_elegibles_por_estado_perfil_sin_estado_no_filtra(self):
        qs = MagicMock()
        assert services.elegibles_por_estado(usuario(estado=""), qs) is qs
        qs.filter.assert_not_called()

    def test_elegibles_por_carrera_sin_carrera_no_filtra(self):
        qs = MagicMock()
        assert services.elegibles_por_carrera(usuario(carrera_id=None), qs) is qs

    def test_carreras_de_interes_une_propia_y_extra(self):
        perfil = MagicMock()
        perfil.carrera_id = 1
        perfil.carreras_extra.values_list.return_value = [2, 3]
        assert services._carreras_de_interes(perfil) == {1, 2, 3}

    def test_carreras_de_interes_sin_carrera_propia(self):
        perfil = MagicMock()
        perfil.carrera_id = None
        perfil.carreras_extra.values_list.return_value = [2]
        assert services._carreras_de_interes(perfil) == {2}

    def test_silenciados_excluye_los_tipos(self):
        qs = MagicMock()
        perfil = NS(categorias_silenciadas=[constants.TIPO_VOLUNTARIADO])
        resultado = services._aplicar_silenciados(perfil, qs)
        qs.exclude.assert_called_once_with(tipo__in=[constants.TIPO_VOLUNTARIADO])
        assert resultado is qs.exclude.return_value

    @pytest.mark.parametrize("silenciadas", [[], None])
    def test_sin_silenciados_no_excluye_nada(self, silenciadas):
        qs = MagicMock()
        perfil = NS(categorias_silenciadas=silenciadas)
        assert services._aplicar_silenciados(perfil, qs) is qs
        qs.exclude.assert_not_called()


# -------------------------------------------------------------------------- rankear
class TestRankear:
    def _rank(self, items, puntajes):
        """Ejecuta rankear con puntuar doblado: {conv.id: puntaje}."""
        with patch.object(services, "puntuar",
                          side_effect=lambda u, c: (puntajes[c.id], [])):
            return [c.id for c, _p, _m in services.rankear(NS(), items)]

    def test_ordena_por_puntaje_descendente(self):
        items = [NS(id=1, transparencia_pct=50), NS(id=2, transparencia_pct=50)]
        assert self._rank(items, {1: 5, 2: 20}) == [2, 1]

    def test_empate_de_puntaje_desempata_por_transparencia(self):
        items = [NS(id=1, transparencia_pct=40), NS(id=2, transparencia_pct=90)]
        assert self._rank(items, {1: 10, 2: 10}) == [2, 1]

    def test_empate_total_desempata_por_id_mas_reciente(self):
        items = [NS(id=1, transparencia_pct=80), NS(id=7, transparencia_pct=80)]
        assert self._rank(items, {1: 10, 7: 10}) == [7, 1]

    def test_lista_vacia_devuelve_lista_vacia(self):
        assert self._rank([], {}) == []


# ------------------------------------------------------------------- con BD (seed)
@pytest.fixture
def base(db):
    call_command("seed_config")
    call_command("seed_taxonomia")
    call_command("seed_elegibilidad")
    empresa = Empresa.objects.create(ruc="20500000009", razon_social="Test SAC",
                                     estado=ESTADO_ACTIVA)
    return NS(empresa=empresa, sistemas=Carrera.objects.get(nombre="Ingeniería de Sistemas"))


def _conv(base, tipo, titulo="C", estado=ESTADO_PUBLICADA, **kw):
    c = Convocatoria.objects.create(empresa=base.empresa, tipo=tipo, titulo=titulo,
                                    estado=estado, **kw)
    c.carreras_objetivo.set([base.sistemas])
    return c


def _egresado(base, username="u", estado="egresado"):
    user = User.objects.create_user(username, email=f"{username}@gmail.com", password="x")
    perfil, _ = PerfilTalento.objects.get_or_create(usuario=user)
    perfil.carrera = base.sistemas
    perfil.estado_academico = estado
    perfil.save()
    return user


@pytest.mark.django_db
class TestConBD:
    def test_tipos_elegibles_estado_desconocido_devuelve_vacio(self, base):
        assert services.tipos_elegibles("estado_inexistente") == set()

    def test_tipos_elegibles_estudiante_incluye_preprofesional(self, base):
        assert constants.TIPO_PRACTICA_PREPROFESIONAL in services.tipos_elegibles("estudiante")

    @pytest.mark.parametrize("estado", [ESTADO_PENDIENTE, ESTADO_OBSERVADA])
    def test_publicadas_excluye_otros_estados(self, base, estado):
        _conv(base, constants.TIPO_EMPLEO, estado=estado)
        assert services.convocatorias_publicadas().count() == 0

    def test_publicadas_incluye_publicada_vigente(self, base):
        _conv(base, constants.TIPO_EMPLEO, fecha_limite=date.today() + timedelta(days=3))
        assert services.convocatorias_publicadas().count() == 1

    def test_publicadas_incluye_fecha_limite_hoy(self, base):  # valor límite
        _conv(base, constants.TIPO_EMPLEO, fecha_limite=date.today())
        assert services.convocatorias_publicadas().count() == 1

    def test_feed_excluye_tipos_silenciados(self, base):
        _conv(base, constants.TIPO_EMPLEO, titulo="Empleo")
        _conv(base, constants.TIPO_VOLUNTARIADO, titulo="Voluntariado")
        user = _egresado(base)
        user.perfil_talento.categorias_silenciadas = [constants.TIPO_VOLUNTARIADO]
        user.perfil_talento.save()
        titulos = {c.titulo for c, _p, _m in services.feed(user)}
        assert titulos == {"Empleo"}

    def test_feed_vacio_si_no_hay_convocatorias(self, base):
        assert services.feed(_egresado(base)) == []

    def test_rankear_credencial_verificada_primero(self, base):
        beca = _conv(base, constants.TIPO_BECA, titulo="Beca")
        _conv(base, constants.TIPO_EMPLEO, titulo="Empleo")
        user = _egresado(base)
        Credencial.objects.create(perfil=user.perfil_talento, tipo="tesis",
                                  detalle="Tesis", fuente=FUENTE_VERIFICADO)
        primero = services.feed(user)[0][0]
        assert primero == beca

    def test_alcance_sin_egresados_es_cero(self, base):
        c = _conv(base, constants.TIPO_EMPLEO)
        assert services.alcance(c) == 0

    def test_alcance_cuenta_solo_los_que_califican(self, base):
        c = _conv(base, constants.TIPO_PRACTICA_PREPROFESIONAL)
        _egresado(base, "est", estado="estudiante")  # califica
        _egresado(base, "egr", estado="egresado")    # no califica en preprofesional
        assert services.alcance(c) == 1