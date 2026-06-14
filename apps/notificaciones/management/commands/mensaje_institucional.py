"""Emite un comunicado institucional (in-app) a los egresados.

Uso:
    python manage.py mensaje_institucional "Texto del comunicado" [--url /ruta/]

El mensaje aparece en la bandeja «Mensajes institucionales» de cada egresado.
"""

from django.core.management.base import BaseCommand

from apps.notificaciones.models import TIPO_GENERAL
from apps.notificaciones.services import notificar
from apps.usuarios.models import PerfilTalento


class Command(BaseCommand):
    help = "Envía un comunicado institucional in-app a todos los egresados."

    def add_arguments(self, parser):
        parser.add_argument("mensaje", help="Texto del comunicado")
        parser.add_argument("--url", default="", help="Enlace opcional (Ver más)")

    def handle(self, *args, **opts):
        mensaje = opts["mensaje"]
        url = opts["url"]
        n = 0
        for talento in PerfilTalento.objects.select_related("usuario"):
            notificar(talento.usuario, mensaje, tipo=TIPO_GENERAL, url=url)
            n += 1
        self.stdout.write(self.style.SUCCESS(f"Comunicado enviado a {n} egresado(s)."))
