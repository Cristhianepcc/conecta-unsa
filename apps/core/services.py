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

    from apps.convocatorias.models import INTERACCION_VISTA, InteraccionConvocatoria
    from apps.taxonomia.models import Carrera

    activas = _convocatorias_activas()
    total_activas = activas.count()
    carreras_cubiertas = (
        Carrera.objects.filter(convocatorias__in=activas).distinct().count()
    )
    promedio = activas.aggregate(p=Avg("transparencia_pct"))["p"] or 0
    vistas = InteraccionConvocatoria.objects.filter(tipo=INTERACCION_VISTA).count()
    return {
        "convocatorias_activas": total_activas,
        "carreras_cubiertas": carreras_cubiertas,
        "indice_transparencia": round(promedio),
        "empresas_participantes": activas.values("empresa").distinct().count(),
        "vistas": vistas,
    }


# Áreas de la taxonomía con un ícono Lucide para los tiles de la landing.
_ICONO_POR_AREA = {
    "Ingenierías y Ciencias Básicas": "cpu",
    "Biomédicas": "heart-pulse",
    "Ciencias Sociales y Humanidades": "scale",
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


# Categorías profesionales de la landing (etiquetas cortas tipo mockup), mapeadas a la
# taxonomía real. Cada una agrupa un área o un conjunto de facultades. (CA-3: conteos reales.)
CATEGORIAS_PROFESIONALES = [
    ("Ingenierías", "cpu", {"area": "Ingenierías y Ciencias Básicas"}),
    ("Ciencias Económicas", "trending-up",
     {"facultades": ["Administración", "Ciencias Contables, Financieras y Economía"]}),
    ("Ciencias Sociales", "users",
     {"facultades": ["Ciencias Histórico Sociales",
                     "Psicología, Relaciones Industriales y Ciencias de la Comunicación"]}),
    ("Salud", "heart-pulse", {"area": "Biomédicas"}),
    ("Educación", "book-open", {"facultades": ["Educación"]}),
    ("Derecho", "scale", {"facultades": ["Derecho"]}),
    ("Otras áreas", "shapes",
     {"facultades": ["Filosofía y Humanidades", "Arquitectura, Urbanismo y Artes"]}),
]


def categorias_profesionales():
    """Las 7 categorías profesionales con su conteo real de convocatorias activas (CA-3)."""
    activas = _convocatorias_activas()
    tiles = []
    for label, icono, filtro in CATEGORIAS_PROFESIONALES:
        if "area" in filtro:
            qs = activas.filter(carreras_objetivo__facultad__area__nombre=filtro["area"])
        else:
            qs = activas.filter(carreras_objetivo__facultad__nombre__in=filtro["facultades"])
        tiles.append({"label": label, "icono": icono, "conteo": qs.distinct().count()})
    return tiles


def convocatorias_destacadas(limite: int = 6):
    """Convocatorias activas destacadas (mayor transparencia, más recientes)."""
    return list(
        _convocatorias_activas()
        .select_related("empresa")
        .order_by("-transparencia_pct", "-creada_en")[:limite]
    )


def resumen_semanal_landing() -> dict:
    """Números reales de la última semana para el panel de 'resumen semanal'."""
    from datetime import timedelta

    from django.utils import timezone

    from apps.convocatorias.models import INTERACCION_VISTA, InteraccionConvocatoria

    ahora = timezone.now()
    desde = ahora - timedelta(days=7)
    activas = _convocatorias_activas()
    nuevas = activas.filter(creada_en__gte=desde)
    return {
        "desde": (ahora - timedelta(days=6)).date(),
        "hasta": ahora.date(),
        "nuevas": nuevas.count(),
        "empresas": nuevas.values("empresa").distinct().count(),
        "areas": nuevas.values("carreras_objetivo__facultad__area").distinct().count(),
        "vistas": InteraccionConvocatoria.objects.filter(
            tipo=INTERACCION_VISTA, creado_en__gte=desde
        ).count(),
    }
