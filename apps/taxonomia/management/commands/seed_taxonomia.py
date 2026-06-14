"""Siembra la taxonomía UNSA: 3 Áreas / 16 Facultades / 43 Carreras + GrupoAfin base.

Idempotente (get_or_create). Datos de ../../taxonomia-unsa.md.

NOTA DE RECONCILIACIÓN (decisión del usuario: ajustar al conteo canónico 16/43):
el detalle de la fuente enumera 17 facultades / 47 carreras, pero el resumen y los
criterios EARS (CA-1, CA-4) fijan 3/16/43 con Ingenierías=19. Para cuadrar:
  - Se omiten 4 carreras: «Ingeniería de Materiales», «Ingeniería Geofísica»,
    «Banca y Seguros», «Artes, Música y Plástica».
  - Se fusiona la Facultad de Economía dentro de «Ciencias Contables, Financieras y Economía»
    (17 → 16 facultades).
Todo es config-as-data: el admin puede reañadir/editar lo que falte sin tocar código.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.taxonomia.models import Area, Carrera, Facultad, GrupoAfin

# Estructura canónica: Área -> Facultad -> [Carreras]
TAXONOMIA = {
    "Ingenierías y Ciencias Básicas": {
        "Producción y Servicios": [
            "Ingeniería de Sistemas",
            "Ciencia de la Computación",
            "Ingeniería Industrial",
            "Ingeniería Mecánica",
            "Ingeniería Eléctrica",
            "Ingeniería Electrónica",
            "Ingeniería de Telecomunicaciones",
        ],
        "Ingeniería Civil": [
            "Ingeniería Civil",
            "Ingeniería Sanitaria",
        ],
        "Ingeniería de Procesos": [
            "Ingeniería Química",
            "Ingeniería Metalúrgica",
            "Ingeniería de Industrias Alimentarias",
            "Ingeniería Ambiental",
        ],
        "Geología, Geofísica y Minas": [
            "Ingeniería Geológica",
            "Ingeniería de Minas",
        ],
        "Ciencias Naturales y Formales": [
            "Física",
            "Matemática",
            "Química",
        ],
        "Arquitectura, Urbanismo y Artes": [
            "Arquitectura",
        ],
    },
    "Biomédicas": {
        "Medicina": ["Medicina"],
        "Enfermería": ["Enfermería"],
        "Ciencias Biológicas y Agropecuarias": [
            "Biología",
            "Agronomía",
            "Ciencias de la Nutrición",
            "Ingeniería Pesquera",
        ],
    },
    "Ciencias Sociales y Humanidades": {
        "Administración": [
            "Administración",
            "Marketing",
            "Gestión",
        ],
        "Ciencias Contables, Financieras y Economía": [
            "Contabilidad",
            "Finanzas",
            "Economía",
        ],
        "Derecho": ["Derecho"],
        "Ciencias Histórico Sociales": [
            "Historia",
            "Sociología",
            "Antropología",
            "Trabajo Social",
            "Turismo y Hotelería",
        ],
        "Educación": ["Educación"],
        "Filosofía y Humanidades": [
            "Filosofía",
            "Literatura",
        ],
        "Psicología, Relaciones Industriales y Ciencias de la Comunicación": [
            "Psicología",
            "Relaciones Industriales",
            "Ciencias de la Comunicación",
        ],
    },
}

# GrupoAfin base: nombre -> lista de carreras miembro.
GRUPOS_AFINES = {
    "Administración o afines": [
        "Administración",
        "Marketing",
        "Gestión",
        "Contabilidad",
        "Finanzas",
        "Economía",
    ],
    "Ingenierías o afines": [
        "Ingeniería de Sistemas",
        "Ciencia de la Computación",
        "Ingeniería Industrial",
        "Ingeniería Electrónica",
        "Ingeniería de Telecomunicaciones",
    ],
    "Salud o afines": [
        "Medicina",
        "Enfermería",
        "Biología",
        "Ciencias de la Nutrición",
        "Psicología",
    ],
}


class Command(BaseCommand):
    help = "Siembra la taxonomía UNSA (3/16/43) y los GrupoAfin base. Idempotente."

    @transaction.atomic
    def handle(self, *args, **options):
        n_areas = n_fac = n_car = 0
        for orden, (area_nombre, facultades) in enumerate(TAXONOMIA.items()):
            area, _ = Area.objects.get_or_create(
                nombre=area_nombre, defaults={"orden": orden}
            )
            n_areas += 1
            for fac_nombre, carreras in facultades.items():
                facultad, _ = Facultad.objects.get_or_create(
                    nombre=fac_nombre, defaults={"area": area}
                )
                n_fac += 1
                for car_nombre in carreras:
                    Carrera.objects.get_or_create(
                        nombre=car_nombre, defaults={"facultad": facultad}
                    )
                    n_car += 1

        n_grupos = 0
        for nombre, miembros in GRUPOS_AFINES.items():
            grupo, _ = GrupoAfin.objects.get_or_create(nombre=nombre)
            carreras = Carrera.objects.filter(nombre__in=miembros)
            grupo.carreras.set(carreras)
            n_grupos += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Taxonomía sembrada: {n_areas} áreas, {n_fac} facultades, "
                f"{n_car} carreras, {n_grupos} grupos afines."
            )
        )
