"""Servicios de notificación: in-app (campana) y resumen semanal por correo (Resend).

Anti-saturación: un solo correo consolidado por egresado (notificaciones.md).
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from apps.matching import services as matching
from apps.usuarios.models import PerfilTalento

from .models import (
    TIPO_GENERAL,
    TIPO_NUEVA_PERTINENTE,
    TIPO_OBSERVADA,
    Notificacion,
    ResumenSemanalLog,
)


# --- In-app -----------------------------------------------------------------
def notificar(usuario, mensaje, *, tipo=TIPO_GENERAL, url=""):
    """Crea una notificación in-app (CA-5)."""
    return Notificacion.objects.create(usuario=usuario, tipo=tipo, mensaje=mensaje, url=url)


def marcar_leidas(usuario, ids=None):
    qs = usuario.notificaciones.filter(leido=False)
    if ids is not None:
        qs = qs.filter(id__in=ids)
    return qs.update(leido=True)


def no_leidas(usuario) -> int:
    if not usuario.is_authenticated:
        return 0
    return usuario.notificaciones.filter(leido=False).count()


def notificar_observacion_convocatoria(conv):
    """Aviso a la empresa cuando su convocatoria es observada (CA-6 de la feature 06)."""
    reclutador = getattr(conv.empresa, "reclutador", None)
    if reclutador is None:
        return None
    return notificar(
        reclutador.usuario,
        f"Tu convocatoria «{conv.titulo}» fue observada: {conv.comentario_revision}",
        tipo=TIPO_OBSERVADA,
    )


# --- Resumen semanal --------------------------------------------------------
def _convocatorias_ya_enviadas(usuario) -> set[int]:
    ids: set[int] = set()
    for log in usuario.resumenes.all():
        ids.update(log.convocatorias.values_list("id", flat=True))
    return ids


def construir_resumen(usuario) -> list:
    """Convocatorias pertinentes y NO enviadas antes a este usuario (vía matching.feed).

    El feed ya aplica Gate 1/2, ranking y categorías silenciadas (CA-1/CA-4).
    """
    enviadas = _convocatorias_ya_enviadas(usuario)
    items = matching.feed(usuario)
    return [conv for conv, _puntaje, _motivos in items if conv.id not in enviadas]


def _enviar_correo(usuario, convocatorias) -> None:
    asunto = "Tu resumen semanal de oportunidades — CONECTA UNSA"
    contexto = {"usuario": usuario, "convocatorias": convocatorias}
    html = render_to_string("notificaciones/resumen_email.html", contexto)
    texto = render_to_string("notificaciones/resumen_email.txt", contexto)
    correo = EmailMultiAlternatives(
        asunto, texto, settings.DEFAULT_FROM_EMAIL, [usuario.email]
    )
    correo.attach_alternative(html, "text/html")
    correo.send()


def enviar_resumen_a(usuario) -> bool:
    """Arma y envía el resumen de un usuario. Devuelve True si envió (CA-1/CA-2/CA-3)."""
    talento = getattr(usuario, "perfil_talento", None)
    if talento is None or talento.frecuencia == "ninguna":
        return False
    if not usuario.email:
        return False

    convocatorias = construir_resumen(usuario)
    if not convocatorias:  # CA-3: sin novedades, no se envía
        return False

    _enviar_correo(usuario, convocatorias)

    log = ResumenSemanalLog.objects.create(usuario=usuario)
    log.convocatorias.set(convocatorias)
    notificar(
        usuario,
        f"Tu resumen semanal tiene {len(convocatorias)} oportunidad(es).",
        tipo=TIPO_NUEVA_PERTINENTE,
        url=reverse("usuarios:dashboard"),
    )
    return True


def enviar_resumenes() -> int:
    """Recorre los egresados con perfil y envía un único correo a cada uno con novedades (CA-1)."""
    enviados = 0
    perfiles = PerfilTalento.objects.exclude(frecuencia="ninguna").select_related("usuario")
    for talento in perfiles:
        if enviar_resumen_a(talento.usuario):
            enviados += 1
    return enviados
