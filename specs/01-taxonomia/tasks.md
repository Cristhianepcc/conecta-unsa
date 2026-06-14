# Tareas — 01 Taxonomía

> Checklist de implementación en orden. Deriva de `design.md`.

## Implementación
- [ ] T1 — Crear app `taxonomia`.
- [ ] T2 — Modelos `Area`, `Facultad`, `Carrera`, `GrupoAfin` + migraciones.
- [ ] T3 — Servicio `expandir(seleccion) -> set[Carrera]` en `taxonomia/services.py`.
- [ ] T4 — Registrar los 4 modelos en Django Admin (con filtros e inline de carreras en Facultad).
- [ ] T5 — Configurar `on_delete=PROTECT` y campo `activa` en Carrera.

## Datos / seed
- [ ] T6 — Comando/fixture que siembra 3 Áreas, 16 Facultades, 43 Carreras (de `taxonomia-unsa.md`)
  y GrupoAfin base ("Administración o afines", "Ingenierías o afines", "Salud o afines").

## Pruebas (criterios EARS → tests)
- [ ] T7 — test CA-1: el seed crea 3/16/43 exactos.
- [ ] T8 — test CA-4: `expandir(Area Ingenierías)` devuelve sus 19 carreras; `expandir(Facultad X)` sus carreras.
- [ ] T9 — test CA-5: eliminar Carrera referenciada lanza `ProtectedError`.
- [ ] T10 — test CA-3: crear GrupoAfin y recuperarlo con sus carreras.

## Cierre
- [ ] Migraciones aplicadas.
- [ ] Definition of Done de la constitución cumplido.
