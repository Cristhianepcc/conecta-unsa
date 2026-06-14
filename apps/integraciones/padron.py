"""Adaptador del padrón académico UNSA (Eje 2 — interoperabilidad).

Frontera de integración con **contrato estable**:

- En DEMO `consultar_dni` resuelve contra `PADRON_DEMO` (datos de ejemplo).
- En PRODUCCIÓN, el cuerpo de `consultar_dni` se reemplaza por la llamada al
  servicio institucional autorizado (PIDE / SUNEDU), devolviendo el **mismo**
  `ResultadoPadron`. La firma no cambia, así las vistas y plantillas que la
  consumen quedan intactas (interoperabilidad sin reescritura).

El DNI es dato personal (Ley 29733): nunca se expone en la credencial pública ni
en los datos que ve una empresa; solo se usa para validar la identidad académica.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

DNI_RE = re.compile(r"^\d{8}$")


@dataclass
class ResultadoPadron:
    """Identidad académica verificada que devuelve el padrón."""

    nombres: str
    carrera_id: int
    carrera: str
    estado_academico: str  # código de apps.core.constants.ESTADOS_ACADEMICOS
    fuente: str = "UNSA"


# DNI -> identidad académica (solo demo). La carrera debe existir en la taxonomía
# sembrada (apps/taxonomia); si no, `consultar_dni` degrada a None (autodeclarado).
PADRON_DEMO = {
    "12345678": {
        "nombres": "María Fernanda Quispe Mamani",
        "carrera": "Ingeniería Industrial",
        "estado": "egresado",
    },
    "87654321": {
        "nombres": "Carlos Andrés Mamani Flores",
        "carrera": "Administración",
        "estado": "titulado",
    },
    "44556677": {
        "nombres": "Lucía Valeria Choque Apaza",
        "carrera": "Ingeniería de Sistemas",
        "estado": "estudiante",
    },
}


def dni_valido(dni: str) -> bool:
    """True si el DNI tiene el formato esperado (8 dígitos)."""
    return bool(DNI_RE.match((dni or "").strip()))


def consultar_dni(dni: str) -> ResultadoPadron | None:
    """Devuelve la identidad académica verificada para un DNI, o None si no existe.

    PRODUCCIÓN: reemplazar el cuerpo por la llamada al servicio PIDE autorizado,
    devolviendo el mismo `ResultadoPadron`.
    """
    fila = PADRON_DEMO.get((dni or "").strip())
    if not fila:
        return None

    from apps.taxonomia.models import Carrera

    carrera = Carrera.objects.filter(nombre=fila["carrera"], activa=True).first()
    if not carrera:
        return None

    return ResultadoPadron(
        nombres=fila["nombres"],
        carrera_id=carrera.id,
        carrera=carrera.nombre,
        estado_academico=fila["estado"],
    )
