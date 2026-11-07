"""Issue #2 - Pruebas unitarias de Dominio (Servicios): apps/convocatorias/services.py

Estilo: pytest + Arrange-Act-Assert. Dobles de prueba con unittest.mock.patch
(equivalente a Mockito) para aislar la lectura de ParametroLegal (RMV, topes).
Las convocatorias se instancian SIN guardar, así no se toca la BD salvo donde se indica.
"""

from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.core.management import call_command

from apps.core import constants
from apps.convocatorias import services
from apps.convocatorias.models import ESTADO_PENDIENTE, Convocatoria
from apps.convocatorias.services import (
    CHECKS_TRANSPARENCIA,
    calcular_transparencia,
    desglose_transparencia,
    faltantes_nivel_1,
    faltantes_transparencia,
    publicar,
    puede_publicar,
    puntos_por_criterio,
    validar_legal,
)

RMV = Decimal("1130")
P_DEC = "apps.convocatorias.services.get_parametro_decimal"
P_INT = "apps.convocatorias.services.get_parametro_int"


# --------------------------------------------------------------------------- helpers
def conv_vacia(**kw):
    """Convocatoria sin guardar y con todos los criterios de transparencia ausentes."""
    base = dict(
        tipo=constants.TIPO_EMPLEO, regimen="D.L. 728", titulo="", descripcion="",
        modalidad="", ubicacion="", duracion_estimada="", fecha_limite=None,
        medio_postulacion="", email_contacto="", no_discriminacion=False,
        vacantes=None, beneficios="", discapacidad=False, salario_confidencial=False,
        banda_salarial_min=None, banda_salarial_max=None,
    )
    base.update(kw)
    return Convocatoria(**base)


def conv_nivel1(**kw):
    """Convocatoria sin guardar con Nivel 1 completo."""
    base = dict(
        titulo="Analista", descripcion="x" * 120, modalidad="remoto", ubicacion="Arequipa",
        duracion_estimada="6 meses", fecha_limite=date.today() + timedelta(days=30),
        medio_postulacion="https://x.pe", email_contacto="rrhh@x.pe", no_discriminacion=True,
    )
    base.update(kw)
    return conv_vacia(**base)


@pytest.fixture
def seeds(db):
    call_command("seed_config")


# ------------------------------------------------------------------- validar_legal
class TestValidarLegal:
    def test_tipo_inexistente_devuelve_error(self):
        errores = validar_legal(conv_vacia(tipo="tipo_inventado"))
        assert errores == ["Tipo de convocatoria no soportado."]

    @patch(P_DEC, return_value=RMV)
    def test_remuneracion_igual_a_rmv_es_valida(self, _m):  # valor límite
        assert validar_legal(conv_vacia(subvencion_remuneracion=RMV)) == []

    @patch(P_DEC, return_value=RMV)
    def test_remuneracion_un_centimo_bajo_rmv_es_error(self, _m):  # valor límite
        errores = validar_legal(conv_vacia(subvencion_remuneracion=Decimal("1129.99")))
        assert any("RMV" in e for e in errores)

    @patch(P_DEC, return_value=RMV)
    def test_remuneracion_none_no_valida_rmv(self, _m):
        assert validar_legal(conv_vacia(subvencion_remuneracion=None)) == []

    @patch(P_DEC, return_value=Decimal("0"))
    def test_sin_rmv_configurada_no_valida_monto(self, _m):
        assert validar_legal(conv_vacia(subvencion_remuneracion=Decimal("1"))) == []

    # --- jornada
    @patch(P_INT, return_value=30)
    def test_preprofesional_jornada_30h_en_el_limite_es_valida(self, _m):
        conv = conv_vacia(tipo=constants.TIPO_PRACTICA_PREPROFESIONAL,
                          requiere_convenio=True, ciclo_minimo=6, jornada_horas=30)
        assert validar_legal(conv) == []

    @patch(P_INT, return_value=30)
    def test_preprofesional_jornada_31h_excede_tope(self, _m):
        conv = conv_vacia(tipo=constants.TIPO_PRACTICA_PREPROFESIONAL,
                          requiere_convenio=True, ciclo_minimo=6, jornada_horas=31)
        assert any("jornada" in e.lower() for e in validar_legal(conv))

    @patch(P_INT, return_value=48)
    def test_profesional_jornada_49h_excede_tope(self, _m):
        conv = conv_vacia(tipo=constants.TIPO_PRACTICA_PROFESIONAL,
                          requiere_convenio=True, tiempo_egreso_meses=12, jornada_horas=49)
        assert any("48" in e for e in validar_legal(conv))

    @patch(P_INT, return_value=48)
    def test_profesional_jornada_48h_es_valida(self, _m):
        conv = conv_vacia(tipo=constants.TIPO_PRACTICA_PROFESIONAL,
                          requiere_convenio=True, tiempo_egreso_meses=12, jornada_horas=48)
        assert validar_legal(conv) == []

    @patch(P_INT, return_value=0)
    def test_tipo_sin_tope_ignora_jornada(self, _m):
        assert validar_legal(conv_vacia(jornada_horas=200)) == []

    # --- campos obligatorios por tipo
    def test_preprofesional_convenio_false_es_error(self):
        conv = conv_vacia(tipo=constants.TIPO_PRACTICA_PREPROFESIONAL,
                          requiere_convenio=False, ciclo_minimo=6)
        assert any("convenio" in e.lower() for e in validar_legal(conv))

    def test_cas_sin_bases_url_es_error(self):
        conv = conv_vacia(tipo=constants.TIPO_CAS, regimen="CAS", bases_url="")
        assert any("bases" in e.lower() for e in validar_legal(conv))

    def test_beca_sin_entidad_otorgante_es_error(self):
        conv = conv_vacia(tipo=constants.TIPO_BECA, entidad_otorgante="")
        assert any("entidad otorgante" in e.lower() for e in validar_legal(conv))

    def test_consultoria_sin_regimen_es_error(self):
        conv = conv_vacia(tipo=constants.TIPO_CONSULTORIA, regimen="   ")
        assert any("régimen" in e.lower() for e in validar_legal(conv))

    # --- voluntariado
    def test_voluntariado_con_monto_cero_es_valido(self):
        conv = conv_vacia(tipo=constants.TIPO_VOLUNTARIADO, subvencion_remuneracion=Decimal("0"))
        assert validar_legal(conv) == []

    def test_voluntariado_con_banda_salarial_es_error(self):
        conv = conv_vacia(tipo=constants.TIPO_VOLUNTARIADO, banda_salarial_min=Decimal("500"))
        assert any("voluntariado" in e.lower() for e in validar_legal(conv))


# ------------------------------------------------------------- transparencia (BD con seed)
class TestTransparencia:
    def test_convocatoria_vacia_da_0(self, seeds):
        assert calcular_transparencia(conv_vacia()) == 0

    def test_descripcion_79_caracteres_no_suma(self, seeds):
        assert calcular_transparencia(conv_vacia(descripcion="x" * 79)) == 0

    def test_descripcion_80_caracteres_suma_su_peso(self, seeds):
        peso = puntos_por_criterio()["descripcion_completa"]
        assert calcular_transparencia(conv_vacia(descripcion="x" * 80)) == peso

    def test_banda_salarial_visible_suma_su_peso(self, seeds):
        conv = conv_vacia(banda_salarial_min=Decimal("2000"), banda_salarial_max=Decimal("3000"))
        assert calcular_transparencia(conv) == puntos_por_criterio()["banda_salarial"]

    def test_banda_incompleta_no_suma(self, seeds):
        conv = conv_vacia(banda_salarial_min=Decimal("2000"), banda_salarial_max=None)
        assert calcular_transparencia(conv) == 0

    def test_todos_los_criterios_dan_100(self, seeds):
        conv = conv_nivel1(
            banda_salarial_min=Decimal("2000"), banda_salarial_max=Decimal("3000"),
            vacantes=2, beneficios="EPS", discapacidad=True,
        )
        assert calcular_transparencia(conv) == 100

    def test_sin_pesos_en_bd_usa_fallback_de_constants(self, db):
        # Sin seed_config: tabla vacía -> usa constants.CRITERIOS_TRANSPARENCIA
        conv = conv_nivel1(
            banda_salarial_min=Decimal("2000"), banda_salarial_max=Decimal("3000"),
            vacantes=2, beneficios="EPS", discapacidad=True,
        )
        assert calcular_transparencia(conv) == 100

    def test_puntos_por_criterio_claves_y_suma(self, seeds):
        puntos = puntos_por_criterio()
        assert set(puntos) == set(CHECKS_TRANSPARENCIA)
        assert 98 <= sum(puntos.values()) <= 102  # tolerancia por redondeo

    def test_desglose_ordena_ausentes_primero_y_por_impacto(self, seeds):
        conv = conv_vacia(descripcion="x" * 120)  # solo 'descripcion_completa' presente
        items = desglose_transparencia(conv)
        assert items[0]["criterio"] == "banda_salarial"  # ausente de mayor peso
        assert items[-1]["criterio"] == "descripcion_completa"  # presentes al final
        assert items[-1]["presente"] is True

    def test_faltantes_solo_devuelve_ausentes(self, seeds):
        conv = conv_vacia(descripcion="x" * 120)
        faltantes = faltantes_transparencia(conv)
        assert all(not i["presente"] for i in faltantes)
        assert "descripcion_completa" not in [i["criterio"] for i in faltantes]
        assert len(faltantes) == len(CHECKS_TRANSPARENCIA) - 1


# ------------------------------------------------------------------ nivel 1 y publicar
class TestPublicacion:
    def test_nivel1_completo_no_tiene_faltantes(self):
        assert faltantes_nivel_1(conv_nivel1()) == []

    def test_falta_titulo_se_reporta(self):
        assert "titulo" in faltantes_nivel_1(conv_nivel1(titulo=""))

    def test_titulo_solo_espacios_cuenta_como_faltante(self):
        assert "titulo" in faltantes_nivel_1(conv_nivel1(titulo="   "))

    def test_falta_fecha_limite_se_reporta(self):
        assert "fecha_limite" in faltantes_nivel_1(conv_nivel1(fecha_limite=None))

    def test_sin_no_discriminacion_se_reporta(self):
        assert "no_discriminacion" in faltantes_nivel_1(conv_nivel1(no_discriminacion=False))

    @patch(P_DEC, return_value=RMV)
    def test_puede_publicar_true_con_todo_ok(self, _m):
        assert puede_publicar(conv_nivel1()) is True

    def test_puede_publicar_false_si_falta_nivel1(self):
        assert puede_publicar(conv_nivel1(titulo="")) is False

    @patch(P_DEC, return_value=RMV)
    def test_puede_publicar_false_si_falla_validacion_legal(self, _m):
        conv = conv_nivel1(subvencion_remuneracion=Decimal("500"))
        assert puede_publicar(conv) is False

    def test_publicar_con_errores_no_cambia_estado(self):
        conv = conv_nivel1(no_discriminacion=False)
        errores = publicar(conv)
        assert any("discriminación" in e.lower() for e in errores)
        assert conv.estado != ESTADO_PENDIENTE

    def test_publicar_campos_faltantes_lista_los_campos(self):
        errores = publicar(conv_nivel1(titulo="", ubicacion=""))
        assert any("titulo" in e and "ubicacion" in e for e in errores)

    @patch(P_DEC, return_value=RMV)
    def test_publicar_acumula_errores_nivel1_y_legales(self, _m):
        conv = conv_nivel1(titulo="", subvencion_remuneracion=Decimal("500"))
        errores = publicar(conv)
        assert len(errores) >= 2