"""Pruebas de servicios de aplicación con dobles (Issue #6)."""

from unittest import TestCase
from unittest.mock import Mock

from .models import ESTADO_ACTIVA, ESTADO_PENDIENTE, ESTADO_RECHAZADA
from .services import activar_empresa, rechazar_empresa


class EmpresaApplicationServiceTests(TestCase):
    def test_activar_empresa_coordina_cambio_y_persistencia(self):
        empresa = Mock(estado=ESTADO_PENDIENTE)

        activar_empresa(empresa)

        self.assertEqual(empresa.estado, ESTADO_ACTIVA)
        empresa.save.assert_called_once_with(update_fields=["estado"])

    def test_rechazar_empresa_coordina_cambio_y_persistencia(self):
        empresa = Mock(estado=ESTADO_PENDIENTE)

        rechazar_empresa(empresa)

        self.assertEqual(empresa.estado, ESTADO_RECHAZADA)
        empresa.save.assert_called_once_with(update_fields=["estado"])
