"""Siembra la matriz de elegibilidad (ReglaElegibilidad) estado × tipo.

Config-as-data (CA-7): el matching la lee de BD; agregar un estado/tipo = filas nuevas,
sin reprogramar. Idempotente.
"""

from django.core.management.base import BaseCommand

from apps.core import constants
from apps.core.models import ReglaElegibilidad


class Command(BaseCommand):
    help = "Siembra la matriz de elegibilidad estado×tipo. Idempotente."

    def handle(self, *args, **options):
        n = 0
        for estado, _ in constants.ESTADOS_ACADEMICOS:
            permitidos = constants.MATRIZ_ELEGIBILIDAD.get(estado, set())
            for tipo, _ in constants.TIPOS_CONVOCATORIA:
                ReglaElegibilidad.objects.update_or_create(
                    estado_academico=estado,
                    tipo_convocatoria=tipo,
                    defaults={"permitido": tipo in permitidos},
                )
                n += 1
        self.stdout.write(
            self.style.SUCCESS(f"Matriz de elegibilidad sembrada: {n} reglas.")
        )
