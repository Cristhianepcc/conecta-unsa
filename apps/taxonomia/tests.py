"""Tests de la feature 01-taxonomia (criterios EARS)."""

from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase

from apps.taxonomia.models import Area, Carrera, Facultad, GrupoAfin
from apps.taxonomia.services import expandir


class TaxonomiaSeedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_taxonomia")

    def test_ca1__seed_crea_3_16_43(self):
        """CA-1: la jerarquía es exactamente 3 áreas / 16 facultades / 43 carreras."""
        self.assertEqual(Area.objects.count(), 3)
        self.assertEqual(Facultad.objects.count(), 16)
        self.assertEqual(Carrera.objects.count(), 43)

    def test_ca6__grupos_afines_base(self):
        """CA-6: se siembra un set base de GrupoAfin."""
        nombres = set(GrupoAfin.objects.values_list("nombre", flat=True))
        self.assertIn("Administración o afines", nombres)
        self.assertIn("Ingenierías o afines", nombres)
        self.assertIn("Salud o afines", nombres)

    def test_ca6__seed_idempotente(self):
        """CA-6: re-ejecutar el seed no duplica datos."""
        call_command("seed_taxonomia")
        self.assertEqual(Area.objects.count(), 3)
        self.assertEqual(Facultad.objects.count(), 16)
        self.assertEqual(Carrera.objects.count(), 43)

    def test_ca4__expandir_area_ingenierias_devuelve_19(self):
        """CA-4: expandir el Área de Ingenierías devuelve sus 19 carreras."""
        area = Area.objects.get(nombre="Ingenierías y Ciencias Básicas")
        carreras = expandir(area)
        self.assertEqual(len(carreras), 19)
        self.assertTrue(all(isinstance(c, Carrera) for c in carreras))

    def test_ca4__expandir_facultad_devuelve_sus_carreras(self):
        """CA-4: expandir una Facultad devuelve solo sus carreras activas."""
        fac = Facultad.objects.get(nombre="Producción y Servicios")
        carreras = expandir(fac)
        self.assertEqual(len(carreras), 7)
        self.assertTrue(all(c.facultad == fac for c in carreras))

    def test_ca4__expandir_excluye_inactivas(self):
        """CA-4: expandir nunca incluye carreras inactivas."""
        fac = Facultad.objects.get(nombre="Ingeniería Civil")
        carrera = fac.carreras.first()
        carrera.activa = False
        carrera.save()
        carreras = expandir(fac)
        self.assertNotIn(carrera, carreras)

    def test_ca4__expandir_grupo_afin(self):
        """CA-4: expandir un GrupoAfin devuelve sus carreras miembro."""
        grupo = GrupoAfin.objects.get(nombre="Salud o afines")
        carreras = expandir(grupo)
        self.assertEqual(carreras, set(grupo.carreras.all()))

    def test_ca4__expandir_mezcla_unica(self):
        """CA-4: expandir una mezcla devuelve un set único (sin duplicados)."""
        area = Area.objects.get(nombre="Biomédicas")
        fac = Facultad.objects.get(nombre="Medicina")  # subconjunto del área
        carreras = expandir([area, fac])
        self.assertEqual(len(carreras), 6)


class TaxonomiaIntegridadTests(TestCase):
    def test_ca3__crear_grupo_afin_y_recuperar(self):
        """CA-3: crear un GrupoAfin con carreras y recuperarlo."""
        area = Area.objects.create(nombre="Área X", orden=1)
        fac = Facultad.objects.create(nombre="Facultad X", area=area)
        c1 = Carrera.objects.create(nombre="Carrera A", facultad=fac)
        c2 = Carrera.objects.create(nombre="Carrera B", facultad=fac)
        grupo = GrupoAfin.objects.create(nombre="Grupo Demo")
        grupo.carreras.set([c1, c2])
        recuperado = GrupoAfin.objects.get(nombre="Grupo Demo")
        self.assertEqual(set(recuperado.carreras.all()), {c1, c2})

    def test_ca5__borrar_carrera_referenciada_protege(self):
        """CA-5: borrar una Facultad referenciada por Carreras lanza ProtectedError."""
        area = Area.objects.create(nombre="Área Y", orden=2)
        fac = Facultad.objects.create(nombre="Facultad Y", area=area)
        Carrera.objects.create(nombre="Carrera Y1", facultad=fac)
        with self.assertRaises(ProtectedError):
            fac.delete()

    def test_ca5__borrar_area_referenciada_protege(self):
        """CA-5: borrar un Área referenciada por Facultades lanza ProtectedError."""
        area = Area.objects.create(nombre="Área Z", orden=3)
        Facultad.objects.create(nombre="Facultad Z", area=area)
        with self.assertRaises(ProtectedError):
            area.delete()
