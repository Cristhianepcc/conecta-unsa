"""Helpers de acceso a la configuración-como-datos y métricas de la landing."""

from decimal import Decimal, InvalidOperation

from .models import ParametroLegal


def get_parametro(clave: str, default: str | None = None) -> str | None:
    """Devuelve el valor (str) de un ParametroLegal, o `default` si no existe."""
    obj = ParametroLegal.objects.filter(clave=clave).first()
    return obj.valor if obj else default


def get_parametro_decimal(clave: str, default: Decimal = Decimal("0")) -> Decimal:
    valor = get_parametro(clave)
    if valor is None:
        return default
    try:
        return Decimal(valor)
    except (InvalidOperation, ValueError):
        return default


def get_parametro_int(clave: str, default: int = 0) -> int:
    valor = get_parametro(clave)
    try:
        return int(valor) if valor is not None else default
    except (ValueError, TypeError):
        return default


# --- Métricas honestas de la landing (feature 09; landing-audit.md) ---------
def _convocatorias_activas():
    """QuerySet de convocatorias publicadas y vigentes (sin cifras infladas, CA-1)."""
    from django.db.models import Q
    from django.utils import timezone

    from apps.convocatorias.models import ESTADO_PUBLICADA, Convocatoria

    hoy = timezone.localdate()
    return Convocatoria.objects.filter(estado=ESTADO_PUBLICADA).filter(
        Q(fecha_limite__gte=hoy) | Q(fecha_limite__isnull=True)
    )


def metricas_landing() -> dict:
    """Cifras calculadas de datos reales sembrados (nunca constantes)."""
    from django.db.models import Avg

    from apps.taxonomia.models import Carrera

    activas = _convocatorias_activas()
    total_activas = activas.count()
    carreras_cubiertas = (
        Carrera.objects.filter(convocatorias__in=activas).distinct().count()
    )
    promedio = activas.aggregate(p=Avg("transparencia_pct"))["p"] or 0
    return {
        "convocatorias_activas": total_activas,
        "carreras_cubiertas": carreras_cubiertas,
        "indice_transparencia": round(promedio),
        "empresas_participantes": activas.values("empresa").distinct().count(),
    }


def categorias_con_conteo():
    """Áreas de la taxonomía con su conteo real de convocatorias activas (CA-3)."""
    from apps.taxonomia.models import Area

    activas = _convocatorias_activas()
    datos = []
    for area in Area.objects.all():
        conteo = activas.filter(carreras_objetivo__facultad__area=area).distinct().count()
        datos.append({"area": area, "conteo": conteo})
    return datos
