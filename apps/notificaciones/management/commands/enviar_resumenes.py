"""Envía el resumen semanal a los egresados con novedades. Para el cron semanal de Railway."""

from django.core.management.base import BaseCommand

from apps.notificaciones.services import enviar_resumenes


class Command(BaseCommand):
    help = "Arma y envía un único correo de resumen por egresado con convocatorias nuevas pertinentes."

    def handle(self, *args, **options):
        n = enviar_resumenes()
        self.stdout.write(self.style.SUCCESS(f"{n} resumen(es) enviado(s)."))
