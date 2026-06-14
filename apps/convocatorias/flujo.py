"""Flujo administrativo de la convocatoria (feature 06; flujo-admin.md).

Máquina de estados, alertas, detección de duplicados (pg_trgm), semáforo de
confianza y caducidad. Todo auditable y sin IA.
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Lower
from django.utils import timezone

from apps.core.services import get_parametro_decimal, get_parametro_int

from .models import (
    ESTADO_BORRADOR,
    ESTADO_CADUCADA,
    ESTADO_OBSERVADA,
    ESTADO_PENDIENTE,
    ESTADO_PUBLICADA,
    ESTADO_RECHAZADA,
    TRANSPARENCIA_ALTA,
    Convocatoria,
)
from .services import faltantes_nivel_1

# --- Alertas ----------------------------------------------------------------
ALERTA_DUPLICADO = "duplicado"
ALERTA_INCOMPLETA = "incompleta"
ALERTA_BAJA_TRANSPARENCIA = "baja_transparencia"
ALERTA_EXCESO = "exceso_difusion"

# --- Máquina de estados (transiciones válidas) ------------------------------
TRANSICIONES = {
    ESTADO_BORRADOR: {ESTADO_PENDIENTE},
    ESTADO_PENDIENTE: {ESTADO_PUBLICADA, ESTADO_OBSERVADA, ESTADO_RECHAZADA},
    ESTADO_PUBLICADA: {ESTADO_OBSERVADA, ESTADO_CADUCADA},
    ESTADO_OBSERVADA: {ESTADO_PENDIENTE, ESTADO_RECHAZADA},
    ESTADO_RECHAZADA: set(),
    ESTADO_CADUCADA: set(),
}


class TransicionInvalida(Exception):
    pass


def mover_estado(conv: Convocatoria, nuevo: str, *, guardar: bool = True) -> Convocatoria:
    """Aplica una transición de estado válida (CA-1) o lanza TransicionInvalida."""
    if nuevo not in TRANSICIONES.get(conv.estado, set()):
        raise TransicionInvalida(f"No se puede pasar de «{conv.estado}» a «{nuevo}».")
    conv.estado = nuevo
    if guardar:
        conv.save(update_fields=["estado"])
    return conv


# --- Detección de duplicados (pg_trgm) --------------------------------------
def detectar_duplicado(conv: Convocatoria):
    """Posibles duplicados: misma empresa + título similar (pg_trgm) + ≤30 días (CA-3).

    Devuelve lista de (convocatoria, similitud) ordenada por similitud desc.
    El admin confirma; el sistema no borra nada.
    """
    umbral = get_parametro_decimal("umbral_similitud_duplicado", Decimal("0.6"))
    desde = timezone.now() - timedelta(days=30)
    titulo = conv.titulo.lower()
    qs = (
        Convocatoria.objects.filter(empresa=conv.empresa, creada_en__gte=desde)
        .exclude(pk=conv.pk)
        .annotate(sim=TrigramSimilarity(Lower("titulo"), titulo))
        .filter(sim__gt=umbral)
        .order_by("-sim")
    )
    return [(o, float(o.sim)) for o in qs]


# --- Alertas ----------------------------------------------------------------
def calcular_alertas(conv: Convocatoria) -> set[str]:
    """Calcula las alertas de una convocatoria (CA-2)."""
    alertas: set[str] = set()

    if faltantes_nivel_1(conv):
        alertas.add(ALERTA_INCOMPLETA)

    if conv.transparencia_pct < 50:
        alertas.add(ALERTA_BAJA_TRANSPARENCIA)

    if conv.pk and detectar_duplicado(conv):
        alertas.add(ALERTA_DUPLICADO)

    limite = get_parametro_int("limite_difusion_30d", 5)
    desde = timezone.now() - timedelta(days=30)
    recientes = (
        Convocatoria.objects.filter(empresa=conv.empresa, creada_en__gte=desde)
        .exclude(pk=conv.pk)
        .count()
    )
    if recientes >= limite:
        alertas.add(ALERTA_EXCESO)

    return alertas


# --- Semáforo de confianza --------------------------------------------------
def decidir_publicacion(conv: Convocatoria) -> str:
    """'auto' si empresa verificada + sin alertas + alta transparencia 🟢; si no 'revision' (CA-4/CA-5)."""
    if (
        conv.empresa.verificada
        and not calcular_alertas(conv)
        and conv.etiqueta_transparencia == TRANSPARENCIA_ALTA
    ):
        return "auto"
    return "revision"


def procesar_envio(conv: Convocatoria) -> str:
    """Envía la convocatoria: auto-publica o deja en pendiente según el semáforo.

    Asume que ya pasó la validación de `services.publicar`. Devuelve el destino aplicado.
    """
    conv.recalcular_transparencia(guardar=False)
    if decidir_publicacion(conv) == "auto":
        conv.estado = ESTADO_PUBLICADA
        conv.fecha_publicacion = timezone.now()
        conv.save()
        return "auto"
    conv.estado = ESTADO_PENDIENTE
    conv.save()
    return "revision"


# --- Acciones del admin -----------------------------------------------------
def aprobar(conv: Convocatoria) -> Convocatoria:
    mover_estado(conv, ESTADO_PUBLICADA, guardar=False)
    conv.fecha_publicacion = timezone.now()
    conv.save(update_fields=["estado", "fecha_publicacion"])
    return conv


def observar(conv: Convocatoria, comentario: str) -> Convocatoria:
    """Devuelve a la empresa con un comentario (CA-6). La notificación se envía en 08."""
    mover_estado(conv, ESTADO_OBSERVADA, guardar=False)
    conv.comentario_revision = comentario
    conv.save(update_fields=["estado", "comentario_revision"])
    _notificar_observacion(conv)
    return conv


def rechazar(conv: Convocatoria, comentario: str = "") -> Convocatoria:
    mover_estado(conv, ESTADO_RECHAZADA, guardar=False)
    if comentario:
        conv.comentario_revision = comentario
    conv.save(update_fields=["estado", "comentario_revision"])
    return conv


def _notificar_observacion(conv: Convocatoria) -> None:
    """Hook de notificación a la empresa (la feature 08 lo implementa)."""
    try:
        from apps.notificaciones.services import notificar_observacion_convocatoria

        notificar_observacion_convocatoria(conv)
    except (ImportError, AttributeError):
        pass  # 08 aún no disponible; el comentario ya quedó registrado.


# --- Caducidad (cron) -------------------------------------------------------
def caducar_vencidas() -> int:
    """Marca como caducadas las convocatorias publicadas cuya fecha límite ya pasó (CA-7)."""
    hoy = timezone.localdate()
    vencidas = Convocatoria.objects.filter(
        estado=ESTADO_PUBLICADA, fecha_limite__lt=hoy
    )
    return vencidas.update(estado=ESTADO_CADUCADA)
