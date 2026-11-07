"""Pruebas de persistencia ORM de Empresa (Issue #4)."""

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase

from apps.convocatorias.models import Convocatoria

from .models import Empresa


class EmpresaRepositoryTests(TestCase):
    def test_empresa_se_puede_recuperar_por_ruc(self):
        Empresa.objects.create(ruc="20444444444", razon_social="Repositorio SAC")

        empresa = Empresa.objects.get(ruc="20444444444")

        self.assertEqual(empresa.razon_social, "Repositorio SAC")

    def test_ruc_unico_impide_duplicados_en_repositorio(self):
        Empresa.objects.create(ruc="20555555555", razon_social="Primera SAC")

        with self.assertRaises(IntegrityError), transaction.atomic():
            Empresa.objects.create(ruc="20555555555", razon_social="Segunda SAC")

    def test_empresa_referenciada_no_se_puede_eliminar(self):
        empresa = Empresa.objects.create(ruc="20666666666", razon_social="Protegida SAC")
        Convocatoria.objects.create(empresa=empresa, tipo="empleo", titulo="Puesto")

        with self.assertRaises(ProtectedError):
            empresa.delete()
