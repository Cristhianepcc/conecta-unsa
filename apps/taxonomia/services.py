"""Lógica de la taxonomía: expansión de cualquier nivel a carreras concretas.

Regla explícita (CA-4): nunca «todas». Área → sus facultades → carreras activas;
Facultad → carreras activas; GrupoAfin → sus carreras (activas); Carrera → ella misma.
"""

from collections.abc import Iterable

from .models import Area, Carrera, Facultad, GrupoAfin


def expandir(seleccion) -> set[Carrera]:
    """Recibe un objeto o iterable de Area/Facultad/Carrera/GrupoAfin y devuelve
    el **set finito** de Carreras activas que abarca."""
    if seleccion is None:
        return set()
    if isinstance(seleccion, (Area, Facultad, Carrera, GrupoAfin)):
        items: Iterable = [seleccion]
    else:
        items = seleccion

    carreras: set[Carrera] = set()
    for item in items:
        if isinstance(item, Carrera):
            if item.activa:
                carreras.add(item)
        elif isinstance(item, Facultad):
            carreras.update(item.carreras.filter(activa=True))
        elif isinstance(item, Area):
            carreras.update(
                Carrera.objects.filter(facultad__area=item, activa=True)
            )
        elif isinstance(item, GrupoAfin):
            carreras.update(item.carreras.filter(activa=True))
        else:
            raise TypeError(f"expandir() no soporta el tipo {type(item).__name__}")
    return carreras
