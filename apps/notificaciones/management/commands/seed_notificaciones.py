"""Siembra notificaciones in-app de demo para que la campana se vea viva. Idempotente.

Se centra en `demo_egresado` (la persona principal de la demo) y añade un par para
`demo_empresa` y `demo_admin`. Mezcla leídas/no leídas (para que el contador de la
campana muestre un número) y escalona `creado_en` (minutos/horas/días atrás) para
que el orden cronológico se vea realista.

Uso:
    python manage.py seed_notificaciones
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone

from apps.convocatorias.models import ESTADO_PUBLICADA, Convocatoria
from apps.notificaciones.models import (
    TIPO_FECHA_LIMITE,
    TIPO_GENERAL,
    TIPO_NUEVA_PERTINENTE,
    TIPO_OBSERVADA,
    TIPO_RESUMEN,
    Notificacion,
)

User = get_user_model()


def _url_conv(conv):
    return reverse("convocatorias:detalle", args=[conv.id]) if conv else ""


class Command(BaseCommand):
    help = "Siembra notificaciones in-app de demo (idempotente)."

    def handle(self, *args, **options):
        ahora = timezone.now()
        total = 0

        # ---- Egresado: convocatorias pertinentes + fecha límite + resumen ----
        egresado = User.objects.filter(username="demo_egresado").first()
        if egresado:
            pub = Convocatoria.objects.filter(estado=ESTADO_PUBLICADA)
            # Convocatorias concretas para enlazar (caen a cualquiera publicada si faltan).
            c_datos = pub.filter(titulo__icontains="Trainee de Datos").first() or pub.first()
            c_mkt = pub.filter(titulo__icontains="Marketing").first() or pub.last()
            c_fin = pub.filter(titulo__icontains="Finanzas").first() or pub.first()

            avisos = [
                # (tipo, mensaje, url, leido, hace)
                (TIPO_NUEVA_PERTINENTE,
                 f"Nueva convocatoria para tu perfil: «{c_datos.titulo}» en {c_datos.empresa}." if c_datos else "Nueva convocatoria pertinente para tu perfil.",
                 _url_conv(c_datos), False, timedelta(minutes=35)),
                (TIPO_NUEVA_PERTINENTE,
                 f"«{c_mkt.titulo}» podría interesarte ({c_mkt.empresa})." if c_mkt else "Una nueva convocatoria coincide con tus intereses.",
                 _url_conv(c_mkt), False, timedelta(hours=5)),
                (TIPO_FECHA_LIMITE,
                 f"Última semana para postular a «{c_fin.titulo}»." if c_fin else "Una convocatoria guardada cierra pronto.",
                 _url_conv(c_fin), False, timedelta(hours=20)),
                (TIPO_RESUMEN,
                 "Tu resumen semanal de oportunidades ya está disponible.",
                 reverse("notificaciones:lista"), True, timedelta(days=2)),
                (TIPO_GENERAL,
                 "Completa tu credencial pública para que las empresas te encuentren.",
                 reverse("usuarios:dashboard"), True, timedelta(days=4)),
            ]
            total += self._sembrar(egresado, avisos, ahora)

        # ---- Empresa: convocatoria observada + bienvenida ----
        empresa_user = User.objects.filter(username="demo_empresa").first()
        if empresa_user:
            avisos = [
                (TIPO_OBSERVADA,
                 "Tu convocatoria fue observada: ajusta la subvención y vuelve a enviarla.",
                 reverse("empresas:dashboard"), False, timedelta(hours=8)),
                (TIPO_GENERAL,
                 "Bienvenido a CONECTA UNSA. Ya puedes publicar tu primera convocatoria.",
                 reverse("empresas:dashboard"), True, timedelta(days=3)),
            ]
            total += self._sembrar(empresa_user, avisos, ahora)

        # ---- Admin: cola de revisión ----
        admin_user = User.objects.filter(username="demo_admin").first()
        if admin_user:
            pendientes = Convocatoria.objects.filter(estado="pendiente").count()
            avisos = [
                (TIPO_GENERAL,
                 f"Tienes {pendientes} convocatoria(s) pendientes de revisión." if pendientes
                 else "No hay convocatorias pendientes de revisión.",
                 reverse("core:panel_admin") if _url_existe("core:panel_admin") else "",
                 False, timedelta(hours=2)),
            ]
            total += self._sembrar(admin_user, avisos, ahora)

        self.stdout.write(self.style.SUCCESS(
            f"Notificaciones sembradas/aseguradas: {total} (en {Notificacion.objects.count()} totales)."
        ))

    def _sembrar(self, usuario, avisos, ahora):
        n = 0
        for tipo, mensaje, url, leido, hace in avisos:
            obj, creado = Notificacion.objects.get_or_create(
                usuario=usuario, mensaje=mensaje,
                defaults={"tipo": tipo, "url": url, "leido": leido},
            )
            if creado:
                # creado_en es auto_now_add; lo escalonamos con un UPDATE directo.
                Notificacion.objects.filter(pk=obj.pk).update(creado_en=ahora - hace)
                n += 1
        return n


def _url_existe(nombre):
    try:
        reverse(nombre)
        return True
    except Exception:  # noqa: BLE001
        return False
