"""Servicios de interacción del egresado con convocatorias (feature 10)."""

from .models import (
    INTERACCION_GUARDADA,
    INTERACCION_VISTA,
    Convocatoria,
    InteraccionConvocatoria,
)


def registrar_vista(usuario, convocatoria) -> None:
    """Registra (idempotente) que el usuario vio la convocatoria (CA-3)."""
    if usuario.is_authenticated:
        InteraccionConvocatoria.objects.update_or_create(
            usuario=usuario, convocatoria=convocatoria, tipo=INTERACCION_VISTA
        )


def alternar_guardada(usuario, convocatoria) -> bool:
    """Guarda o quita de guardadas. Devuelve True si quedó guardada (CA-4)."""
    obj, creado = InteraccionConvocatoria.objects.get_or_create(
        usuario=usuario, convocatoria=convocatoria, tipo=INTERACCION_GUARDADA
    )
    if not creado:
        obj.delete()
        return False
    return True


def _convocatorias_por_interaccion(usuario, tipo):
    return Convocatoria.objects.filter(
        interacciones__usuario=usuario, interacciones__tipo=tipo
    ).order_by("-interacciones__creado_en").distinct()


def guardadas_de(usuario):
    return _convocatorias_por_interaccion(usuario, INTERACCION_GUARDADA)


def historial_de(usuario):
    return _convocatorias_por_interaccion(usuario, INTERACCION_VISTA)


def ids_guardadas(usuario) -> set:
    """IDs de convocatorias guardadas por el usuario (para marcar tarjetas en lote)."""
    if not usuario.is_authenticated:
        return set()
    return set(
        InteraccionConvocatoria.objects.filter(
            usuario=usuario, tipo=INTERACCION_GUARDADA
        ).values_list("convocatoria_id", flat=True)
    )


def esta_guardada(usuario, convocatoria) -> bool:
    if not usuario.is_authenticated:
        return False
    return InteraccionConvocatoria.objects.filter(
        usuario=usuario, convocatoria=convocatoria, tipo=INTERACCION_GUARDADA
    ).exists()
