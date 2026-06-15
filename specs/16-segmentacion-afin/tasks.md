# Tareas — 16 Segmentación por carreras afines

> Deriva de `design.md`.

## Implementación
- [ ] T1 — Añadir `grupos_afines` (ModelMultipleChoiceField, no-modelo) a `ConvocatoriaForm`.
- [ ] T2 — Helper `_expandir_grupos()` reusando `taxonomia.services.carreras_de`.
- [ ] T3 — Sobrescribir `ConvocatoriaForm.save()` para expandir grupos → `carreras_objetivo` (unión).
- [ ] T4 — UI en `_form.html`: multiselect de grupos afines en el bloque "Dirigida a" + ayuda.

## Datos / seed
- [ ] T5 — Verificar que `seed_taxonomia` deja los `GRUPOS_AFINES` poblados (ya existe).

## Pruebas (criterios EARS → tests)
- [ ] T6 — test CA-1: publicar con grupo → `carreras_objetivo` contiene a todos los miembros.
- [ ] T7 — test CA-2: egresado de carrera miembro ve la convocatoria en el feed.
- [ ] T8 — test CA-3: grupo + carrera suelta → unión sin duplicados.
- [ ] T9 — test CA-4: cambiar el grupo no altera convocatorias ya publicadas.

## Cierre
- [ ] Sin migraciones nuevas (no cambia el modelo).
- [ ] Definition of Done de la constitución cumplido.
