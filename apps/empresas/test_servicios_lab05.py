"""Pruebas unitarias de los servicios de dominio de Empresa (Issue #2)."""

from types import SimpleNamespace

from unittest import TestCase

from .models import ESTADO_ACTIVA, ESTADO_PENDIENTE
from .services import empresa_de, empresa_puede_publicar


class EmpresaServiceTests(TestCase):
    def test_empresa_puede_publicar_solo_si_esta_activa(self):
        self.assertFalse(empresa_puede_publicar(None))
        self.assertFalse(empresa_puede_publicar(SimpleNamespace(estado=ESTADO_PENDIENTE)))
        self.assertTrue(empresa_puede_publicar(SimpleNamespace(estado=ESTADO_ACTIVA)))

    def test_empresa_de_devuelve_la_empresa_del_reclutador(self):
        empresa = object()
        usuario = SimpleNamespace(reclutador=SimpleNamespace(empresa=empresa))

        self.assertIs(empresa_de(usuario), empresa)

    def test_empresa_de_devuelve_none_sin_reclutador(self):
        self.assertIsNone(empresa_de(SimpleNamespace()))
