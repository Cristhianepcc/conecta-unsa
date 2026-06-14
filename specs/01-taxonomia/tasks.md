# Tareas — 01 Taxonomía

> Checklist de implementación en orden. Deriva de `design.md`.

## Implementación
- [x] T1 — Crear app `taxonomia`.
- [x] T2 — Modelos `Area`, `Facultad`, `Carrera`, `GrupoAfin` + migraciones.
- [x] T3 — Servicio `expandir(seleccion) -> set[Carrera]` en `taxonomia/services.py`.
- [x] T4 — Registrar los 4 modelos en Django Admin (con filtros e inline de carreras en Facultad).
- [x] T5 — Configurar `on_delete=PROTECT` y campo `activa` en Carrera.

## Datos / seed
- [x] T6 — Comando `seed_taxonomia` que siembra 3 Áreas, 16 Facultades, 43 Carreras
  y GrupoAfin base ("Administración o afines", "Ingenierías o afines", "Salud o afines").

## Pruebas (criterios EARS → tests)
- [x] T7 — test CA-1: el seed crea 3/16/43 exactos.
- [x] T8 — test CA-4: `expandir(Area Ingenierías)` devuelve sus 19 carreras; `expandir(Facultad X)` sus carreras.
- [x] T9 — test CA-5: eliminar referencia lanza `ProtectedError`.
- [x] T10 — test CA-3: crear GrupoAfin y recuperarlo con sus carreras.

## Cierre
- [x] Migraciones aplicadas.
- [x] Definition of Done de la constitución cumplido.

> Nota de reconciliación (decisión del usuario, "ajustar a 16/43"): el detalle de
> `taxonomia-unsa.md` enumera 17 fac / 47 carreras; se ajustó al conteo canónico (3/16/43)
> omitiendo 4 carreras (Ing. de Materiales, Ing. Geofísica, Banca y Seguros, Artes-Música-Plástica)
> y fusionando la Facultad de Economía en «Ciencias Contables, Financieras y Economía».
> Todo editable en el panel admin (config-as-data). 11 tests EARS verdes.
