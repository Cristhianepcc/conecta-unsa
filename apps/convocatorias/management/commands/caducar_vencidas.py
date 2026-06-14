"""Marca como caducadas las convocatorias vencidas (CA-7). Para cron diario."""

from django.core.management.base import BaseCommand

from apps.convocatorias.flujo import caducar_vencidas


class Command(BaseCommand):
    help = "Marca como caducadas las convocatorias publicadas cuya fecha límite ya pasó."

    def handle(self, *args, **options):
        n = caducar_vencidas()
        self.stdout.write(self.style.SUCCESS(f"{n} convocatoria(s) marcada(s) como caducada(s)."))
