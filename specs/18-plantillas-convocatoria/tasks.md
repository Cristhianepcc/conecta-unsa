# Tareas — 18 Plantillas reutilizables de convocatoria

> Deriva de `design.md`.

## Implementación
- [ ] T1 — Modelo `PlantillaConvocatoria` (nombre, tipo, activa, valores JSON) + migración.
- [ ] T2 — Registrar en Django Admin con validación de `valores` contra campos del form.
- [ ] T3 — Servicios `plantillas_activas()` e `initial_desde_plantilla()`.
- [ ] T4 — Vista publicar: leer `?plantilla=<id>` → `ConvocatoriaForm(initial=...)`.
- [ ] T5 — UI: selector de plantillas (paso 0) + banner "Partiste de la plantilla X".
- [ ] T6 — Cambiar "Guía y plantillas" del sidebar para enlazar al selector real.

## Datos / seed
- [ ] T7 — Seed de plantillas base (práctica, empleo, voluntariado, beca/servicio).

## Pruebas (criterios EARS → tests)
- [ ] T8 — test CA-2: publicar con `?plantilla` → form pre-llenado.
- [ ] T9 — test CA-3: editar un campo pre-llenado → se guarda el valor editado.
- [ ] T10 — test CA-4: publicar sin plantilla → form en blanco funciona.

## Cierre
- [ ] Migración aplicada; modelo propuesto en `modelo-datos.md`.
- [ ] Definition of Done de la constitución cumplido.
