"""Matching: qué convocatorias ve cada usuario y en qué orden (matching.md).

Tres niveles, todos por reglas transparentes y explicables (sin IA):
- Gate 1: estado académico × tipo (elegibilidad legal, ReglaElegibilidad config-as-data).
- Gate 2: carrera (segmentación; carrera del egresado + carreras_extra de interés).
- Layer 3: ranking por afinidad de credenciales + preferencias, con motivo legible.
"""

from django.db.models import Q
from django.utils import timezone

from apps.core import constants
from apps.core.models import ReglaElegibilidad
from apps.convocatorias.models import ESTADO_PUBLICADA, Convocatoria

# Relevancia: tipo de credencial → tipos de convocatoria que potencia (matching.md Layer 3).
RELEVANCIA_CREDENCIAL = {
    "idioma": {constants.TIPO_EMPLEO, constants.TIPO_TRAINEE, constants.TIPO_CONSULTORIA},
    "articulo": {constants.TIPO_BECA},
    "tesis": {constants.TIPO_BECA},
    "representacion": {constants.TIPO_TRAINEE},
    "incubadora_jaku": {constants.TIPO_CONSULTORIA, constants.TIPO_TRAINEE},
    "intercambio": {constants.TIPO_EMPLEO, constants.TIPO_TRAINEE},
    "olimpiada": {constants.TIPO_BECA, constants.TIPO_TRAINEE},
    "voluntariado": {constants.TIPO_VOLUNTARIADO},
    "practica_convalidada": {constants.TIPO_EMPLEO, constants.TIPO_PRACTICA_PROFESIONAL},
}

PESO_CREDENCIAL = 10
PESO_CREDENCIAL_VERIFICADA = 15  # mayor confianza (matching.md: verificado > autodeclarado)
PESO_TIPO_PREFERIDO = 12

# Etiqueta corta de cada credencial para los chips de "por qué te recomendamos".
CHIP_CREDENCIAL = {
    "idioma": "Idioma",
    "representacion": "Liderazgo",
    "tesis": "Investigación",
    "articulo": "Investigación",
    "practica_convalidada": "Experiencia previa",
    "incubadora_jaku": "Innovación",
    "intercambio": "Internacional",
    "olimpiada": "Excelencia",
    "voluntariado": "Voluntariado",
}


def _perfil_talento(usuario):
    return getattr(usuario, "perfil_talento", None)


def compatibilidad(usuario, conv):
    """% de compatibilidad (0-100) + chips de motivos cortos para la tarjeta de oportunidad.

    Base por haber pasado los gates (elegibilidad + carrera); bonus por carrera propia,
    credenciales afines y tipo preferido. Explicable (sin IA).
    """
    perfil = _perfil_talento(usuario)
    pct = 55
    chips: list[str] = []
    if not perfil:
        return pct, chips

    if perfil.carrera_id and conv.carreras_objetivo.filter(id=perfil.carrera_id).exists():
        pct += 15
        chips.append(str(perfil.carrera))
    elif perfil.carrera_id:
        pct += 6  # llega por carrera afín de interés

    for cred in perfil.credenciales.all():
        if conv.tipo in RELEVANCIA_CREDENCIAL.get(cred.tipo, set()):
            pct += 8 if cred.verificada else 6
            chip = CHIP_CREDENCIAL.get(cred.tipo, cred.get_tipo_display())
            if chip not in chips:
                chips.append(chip)

    if conv.tipo in (perfil.tipos_preferidos or []):
        pct += 8
        chips.append("Tipo preferido")

    return min(pct, 100), chips


def convocatorias_publicadas():
    """Publicadas y vigentes: estado publicada y fecha límite no vencida (feature 13).

    Defensa en profundidad: aunque el cron `caducar_vencidas` no haya corrido aún, el
    egresado nunca ve ni recibe convocatorias vencidas en el feed ni en el resumen
    (ambos parten de aquí). Sin `fecha_limite` (null) = no expira.
    """
    hoy = timezone.localdate()
    return Convocatoria.objects.filter(estado=ESTADO_PUBLICADA).filter(
        Q(fecha_limite__gte=hoy) | Q(fecha_limite__isnull=True)
    )


def tipos_elegibles(estado_academico: str) -> set[str]:
    """Tipos permitidos para un estado según ReglaElegibilidad (CA-1/CA-7)."""
    if not estado_academico:
        return set()
    return set(
        ReglaElegibilidad.objects.filter(
            estado_academico=estado_academico, permitido=True
        ).values_list("tipo_convocatoria", flat=True)
    )


def elegibles_por_estado(usuario, qs=None):
    """Gate 1: excluye tipos no elegibles para el estado académico (CA-1)."""
    qs = convocatorias_publicadas() if qs is None else qs
    perfil = _perfil_talento(usuario)
    if not perfil or not perfil.estado_academico:
        return qs  # sin estado conocido no se aplica el filtro (CA-5)
    return qs.filter(tipo__in=tipos_elegibles(perfil.estado_academico))


def _carreras_de_interes(perfil):
    ids = set()
    if perfil.carrera_id:
        ids.add(perfil.carrera_id)
    ids.update(perfil.carreras_extra.values_list("id", flat=True))
    return ids


def elegibles_por_carrera(usuario, qs=None):
    """Gate 2: solo convocatorias cuyas carreras objetivo incluyen la carrera del usuario
    (o sus carreras extra de interés). CA-2."""
    qs = convocatorias_publicadas() if qs is None else qs
    perfil = _perfil_talento(usuario)
    if not perfil or not perfil.carrera_id:
        return qs  # sin carrera no se aplica el filtro (CA-5)
    carreras = _carreras_de_interes(perfil)
    return qs.filter(carreras_objetivo__in=carreras).distinct()


def _aplicar_silenciados(perfil, qs):
    silenciados = perfil.categorias_silenciadas or []
    if silenciados:
        qs = qs.exclude(tipo__in=silenciados)
    return qs


def puntuar(usuario, conv):
    """Devuelve (puntaje, motivos) explicables para una convocatoria (CA-3/CA-4)."""
    perfil = _perfil_talento(usuario)
    puntaje = 0
    motivos: list[str] = []
    if not perfil:
        return puntaje, motivos

    for cred in perfil.credenciales.all():
        tipos_potenciados = RELEVANCIA_CREDENCIAL.get(cred.tipo, set())
        if conv.tipo in tipos_potenciados:
            peso = PESO_CREDENCIAL_VERIFICADA if cred.verificada else PESO_CREDENCIAL
            puntaje += peso
            # Motivo conciso: solo la credencial (sin repetir "coincide con tu credencial").
            motivos.append(cred.detalle or cred.get_tipo_display())

    if conv.tipo in (perfil.tipos_preferidos or []):
        puntaje += PESO_TIPO_PREFERIDO
        motivos.append("tipo que prefieres")

    return puntaje, motivos


def rankear(usuario, qs=None):
    """Layer 3: ordena las convocatorias por afinidad (no oculta nada). CA-3/CA-4.

    Devuelve lista de tuplas (convocatoria, puntaje, motivos). Empate → más recientes primero.
    """
    qs = convocatorias_publicadas() if qs is None else qs
    items = []
    for conv in qs:
        puntaje, motivos = puntuar(usuario, conv)
        items.append((conv, puntaje, motivos))
    items.sort(key=lambda t: (-t[1], -t[0].transparencia_pct, -t[0].id))
    return items


def feed(usuario):
    """Compone Gate 1 + Gate 2 + Layer 3 y devuelve la lista ordenada (CA-5: tolera perfil incompleto)."""
    qs = convocatorias_publicadas()
    qs = elegibles_por_estado(usuario, qs)
    qs = elegibles_por_carrera(usuario, qs)
    perfil = _perfil_talento(usuario)
    if perfil:
        qs = _aplicar_silenciados(perfil, qs)
    return rankear(usuario, qs)


def alcance(convocatoria) -> int:
    """Conteo de egresados cuyas carrera y estado califican para la convocatoria (CA-6)."""
    from apps.usuarios.models import PerfilTalento

    estados_que_califican = list(
        ReglaElegibilidad.objects.filter(
            tipo_convocatoria=convocatoria.tipo, permitido=True
        ).values_list("estado_academico", flat=True)
    )
    carreras_ids = convocatoria.carreras_objetivo.values_list("id", flat=True)
    return (
        PerfilTalento.objects.filter(
            carrera_id__in=carreras_ids, estado_academico__in=estados_que_califican
        )
        .distinct()
        .count()
    )
