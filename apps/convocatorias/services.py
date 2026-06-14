"""Lógica de convocatorias: requisitos por tipo, validación legal y transparencia.

Reglas transparentes y auditables (sin IA). Los montos/topes/pesos vienen de
config-as-data (ParametroLegal, PesoTransparencia), nunca hardcodeados.
"""

from decimal import Decimal

from apps.core import constants
from apps.core.services import get_parametro_decimal, get_parametro_int
from apps.core.models import PesoTransparencia

from .models import (
    ESTADO_PENDIENTE,
    Convocatoria,
)

# Pago esperado por tipo (modelo-datos.md §2, fila «Subvención/Remuneración/Honorario»).
PAGO_SUBVENCION = "subvencion"   # ≥ RMV (referencial mínimo de práctica)
PAGO_RMV = "rmv"                 # sueldo ≥ RMV
PAGO_HONORARIO = "honorario"     # honorario libre
PAGO_BECA = "beca"               # monto de beca
PAGO_BLOQUEADO = "bloqueado"     # voluntariado: sin remuneración (CA-5)

# Reglas por tipo: campos Nivel 2 obligatorios + regla de pago + tope de jornada.
REGLAS_POR_TIPO = {
    constants.TIPO_PRACTICA_PREPROFESIONAL: {
        "requeridos": ["requiere_convenio", "ciclo_minimo"],
        "pago": PAGO_SUBVENCION,
        "tope_jornada_param": "tope_jornada_practica_preprofesional",
    },
    constants.TIPO_PRACTICA_PROFESIONAL: {
        "requeridos": ["requiere_convenio", "tiempo_egreso_meses"],
        "pago": PAGO_SUBVENCION,
        "tope_jornada_param": "tope_jornada_practica_profesional",
    },
    constants.TIPO_TRAINEE: {
        "requeridos": ["regimen"],
        "pago": PAGO_RMV,
        "tope_jornada_param": None,
    },
    constants.TIPO_EMPLEO: {
        "requeridos": ["regimen"],
        "pago": PAGO_RMV,
        "tope_jornada_param": None,
    },
    constants.TIPO_CAS: {
        "requeridos": ["regimen", "bases_url"],
        "pago": PAGO_HONORARIO,
        "tope_jornada_param": None,
    },
    constants.TIPO_VOLUNTARIADO: {
        "requeridos": [],
        "pago": PAGO_BLOQUEADO,
        "tope_jornada_param": None,
    },
    constants.TIPO_BECA: {
        "requeridos": ["entidad_otorgante"],
        "pago": PAGO_BECA,
        "tope_jornada_param": None,
    },
    constants.TIPO_CONSULTORIA: {
        "requeridos": ["regimen"],
        "pago": PAGO_HONORARIO,
        "tope_jornada_param": None,
    },
}

# Etiquetas legibles para los campos requeridos (para mensajes).
ETIQUETAS_CAMPO = {
    "requiere_convenio": "convenio UNSA",
    "ciclo_minimo": "ciclo/semestre mínimo",
    "tiempo_egreso_meses": "tiempo máx. de egreso",
    "regimen": "régimen laboral",
    "bases_url": "bases + cronograma",
    "entidad_otorgante": "entidad otorgante",
}

# Campos Nivel 1 obligatorios para publicar (modelo-datos.md §2, Nivel 1).
CAMPOS_NIVEL_1 = [
    "titulo", "descripcion", "modalidad", "ubicacion", "duracion_estimada",
    "fecha_limite", "medio_postulacion", "email_contacto",
]


def campos_requeridos(tipo: str) -> list[str]:
    """Campos Nivel 2 obligatorios para el `tipo` dado (CA-3)."""
    return list(REGLAS_POR_TIPO.get(tipo, {}).get("requeridos", []))


def _campo_presente(conv: Convocatoria, campo: str) -> bool:
    valor = getattr(conv, campo, None)
    if campo == "requiere_convenio":
        # El convenio es obligatorio → debe declararse como requerido (True).
        return valor is True
    if valor is None:
        return False
    if isinstance(valor, str):
        return valor.strip() != ""
    return True


def validar_legal(conv: Convocatoria) -> list[str]:
    """Valida reglas legales por tipo. Devuelve lista de errores (vacía si OK).

    Cubre CA-3 (campos según tipo), CA-4 (pago ≥ RMV) y CA-5 (voluntariado sin pago).
    """
    errores: list[str] = []
    regla = REGLAS_POR_TIPO.get(conv.tipo)
    if not regla:
        errores.append("Tipo de convocatoria no soportado.")
        return errores

    # CA-3: campos Nivel 2 obligatorios según el tipo.
    for campo in regla["requeridos"]:
        if not _campo_presente(conv, campo):
            etiqueta = ETIQUETAS_CAMPO.get(campo, campo)
            errores.append(f"Para este tipo es obligatorio: {etiqueta}.")

    pago = regla["pago"]
    monto = conv.subvencion_remuneracion

    # CA-5: el voluntariado no admite remuneración.
    if pago == PAGO_BLOQUEADO:
        if (monto and monto > 0) or conv.banda_salarial_min or conv.banda_salarial_max:
            errores.append("El voluntariado no puede ofrecer remuneración.")
    # CA-4: subvención/remuneración no puede ser menor a la RMV.
    elif pago in (PAGO_SUBVENCION, PAGO_RMV):
        if monto is not None:
            rmv = get_parametro_decimal("rmv", Decimal("0"))
            if rmv and monto < rmv:
                errores.append(
                    f"La subvención/remuneración (S/ {monto}) no puede ser menor a la RMV "
                    f"vigente (S/ {rmv})."
                )

    # Tope de jornada por tipo.
    tope_param = regla["tope_jornada_param"]
    if tope_param and conv.jornada_horas is not None:
        tope = get_parametro_int(tope_param, 0)
        if tope and conv.jornada_horas > tope:
            errores.append(
                f"La jornada ({conv.jornada_horas} h/sem) excede el tope legal de {tope} h/sem."
            )

    return errores


# --- Transparencia ----------------------------------------------------------
def _check_banda_salarial(c):
    return bool(c.banda_salarial_min and c.banda_salarial_max and not c.salario_confidencial)


def _check_descripcion(c):
    return len(c.descripcion.strip()) >= 80


def _check_duracion(c):
    return bool(c.duracion_estimada.strip())


def _check_modalidad_ubicacion(c):
    return bool(c.modalidad and c.ubicacion.strip())


def _check_vacantes(c):
    return bool(c.vacantes and c.vacantes > 0)


def _check_beneficios(c):
    return bool(c.beneficios.strip())


def _check_contacto(c):
    return bool(c.email_contacto.strip() or c.medio_postulacion.strip())


def _check_discapacidad(c):
    return bool(c.discapacidad)


CHECKS_TRANSPARENCIA = {
    "banda_salarial": _check_banda_salarial,
    "descripcion_completa": _check_descripcion,
    "duracion": _check_duracion,
    "modalidad_ubicacion": _check_modalidad_ubicacion,
    "vacantes": _check_vacantes,
    "beneficios": _check_beneficios,
    "contacto": _check_contacto,
    "discapacidad": _check_discapacidad,
}


def calcular_transparencia(conv: Convocatoria) -> int:
    """% de transparencia ponderado con los PesoTransparencia configurables (CA-6).

    Usa el seed de pesos si está disponible; si no hay pesos en BD, cae a los
    valores canónicos de constants (para no romper en entornos sin seed).
    """
    pesos = list(PesoTransparencia.objects.all())
    if not pesos:
        pesos = [
            PesoTransparencia(criterio=c, etiqueta=e, peso=p)
            for c, e, p in constants.CRITERIOS_TRANSPARENCIA
        ]

    total = sum(p.peso for p in pesos) or 1
    presente = 0
    for p in pesos:
        check = CHECKS_TRANSPARENCIA.get(p.criterio)
        if check and check(conv):
            presente += p.peso

    return round(presente / total * 100)


def desglose_transparencia(conv: Convocatoria) -> list[dict]:
    """Desglose por criterio para coaching (CA-6): cuánto suma cada uno y si está presente.

    Ordena ausentes primero y por impacto (puntos) descendente, para responder
    "qué te falta y cuánto subiría tu % de transparencia".
    """
    pesos = list(PesoTransparencia.objects.all())
    if not pesos:
        pesos = [
            PesoTransparencia(criterio=c, etiqueta=e, peso=p)
            for c, e, p in constants.CRITERIOS_TRANSPARENCIA
        ]
    total = sum(p.peso for p in pesos) or 1
    items = []
    for p in pesos:
        check = CHECKS_TRANSPARENCIA.get(p.criterio)
        items.append(
            {
                "criterio": p.criterio,
                "etiqueta": p.etiqueta,
                "puntos": round(p.peso / total * 100),
                "presente": bool(check and check(conv)),
            }
        )
    items.sort(key=lambda i: (i["presente"], -i["puntos"]))
    return items


def faltantes_transparencia(conv: Convocatoria) -> list[dict]:
    """Criterios de transparencia ausentes, mayor impacto primero."""
    return [i for i in desglose_transparencia(conv) if not i["presente"]]


def puntos_por_criterio() -> dict[str, int]:
    """Puntos (%) que aporta cada criterio de transparencia, desde config-as-data.

    Sin convocatoria: alimenta el coaching en vivo del formulario (la barra de
    transparencia que sube mientras la empresa completa campos). Mismas claves que
    CHECKS_TRANSPARENCIA, para que el cálculo del cliente sea fiel al del servidor.
    """
    pesos = list(PesoTransparencia.objects.all())
    if not pesos:
        pesos = [
            PesoTransparencia(criterio=c, etiqueta=e, peso=p)
            for c, e, p in constants.CRITERIOS_TRANSPARENCIA
        ]
    total = sum(p.peso for p in pesos) or 1
    return {p.criterio: round(p.peso / total * 100) for p in pesos}


# --- Publicación ------------------------------------------------------------
def faltantes_nivel_1(conv: Convocatoria) -> list[str]:
    """Campos Nivel 1 que faltan para poder publicar (CA-2)."""
    faltan = [campo for campo in CAMPOS_NIVEL_1 if not _campo_presente(conv, campo)]
    if not conv.no_discriminacion:  # CA-10
        faltan.append("no_discriminacion")
    return faltan


def puede_publicar(conv: Convocatoria) -> bool:
    """True si tiene Nivel 1 completo, no_discriminacion y pasa la validación legal."""
    return not faltantes_nivel_1(conv) and not validar_legal(conv)


def publicar(conv: Convocatoria) -> list[str]:
    """Intenta enviar la convocatoria a revisión (estado pendiente).

    Devuelve lista de errores; si está vacía, la convocatoria quedó en `pendiente`.
    """
    errores = []
    faltan = faltantes_nivel_1(conv)
    if faltan:
        if "no_discriminacion" in faltan:
            errores.append("Debes aceptar la declaración de no discriminación (Ley 26772).")
        otros = [f for f in faltan if f != "no_discriminacion"]
        if otros:
            errores.append("Faltan campos fundamentales: " + ", ".join(otros) + ".")
    errores.extend(validar_legal(conv))

    if errores:
        return errores

    conv.recalcular_transparencia(guardar=False)
    conv.estado = ESTADO_PENDIENTE
    conv.save()
    return []
