"""Siembra la configuración-como-datos base: parámetros legales y pesos de
transparencia (modelo-datos.md §4 y §6). Idempotente.

La matriz de elegibilidad (ReglaElegibilidad) la siembra la feature 05-matching.
"""

from django.core.management.base import BaseCommand

from apps.core import constants
from apps.core.models import ParametroLegal, PesoTransparencia


class Command(BaseCommand):
    help = "Siembra ParametroLegal y PesoTransparencia base. Idempotente."

    def handle(self, *args, **options):
        for clave, valor, descripcion in constants.PARAMETROS_LEGALES_BASE:
            ParametroLegal.objects.update_or_create(
                clave=clave, defaults={"valor": valor, "descripcion": descripcion}
            )

        for criterio, etiqueta, peso in constants.CRITERIOS_TRANSPARENCIA:
            PesoTransparencia.objects.update_or_create(
                criterio=criterio, defaults={"etiqueta": etiqueta, "peso": peso}
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Config sembrada: {ParametroLegal.objects.count()} parámetros legales, "
                f"{PesoTransparencia.objects.count()} pesos de transparencia."
            )
        )
