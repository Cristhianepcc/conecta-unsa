"""Verificación de configuración de unittest.mock (Issue #5)."""

from unittest import TestCase
from unittest.mock import Mock


class MockingConfigurationTests(TestCase):
    def test_mock_reemplaza_un_colaborador_y_registra_la_interaccion(self):
        repositorio = Mock()
        repositorio.buscar_por_ruc.return_value = {"ruc": "20123456789"}

        resultado = repositorio.buscar_por_ruc("20123456789")

        self.assertEqual(resultado["ruc"], "20123456789")
        repositorio.buscar_por_ruc.assert_called_once_with("20123456789")
