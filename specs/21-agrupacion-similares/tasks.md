# Tareas — 21 Agrupación de convocatorias similares

> Deriva de `design.md`.

## Implementación
- [ ] T1 — `apps/convocatorias/agrupacion.py`: `agrupar_similares()` (tipo + carrera + ventana).
- [ ] T2 — Integrar en el digest: `enviar_resumen_a` agrupa antes de renderizar.
- [ ] T3 — Render de grupos en `resumen_email.html` / `.txt` ("y N más similares").
- [ ] T4 — (Opcional) toggle "agrupar similares" en la bandeja admin.

## Datos / seed
- [ ] T5 — Parámetro `agrupacion_ventana_dias` (14) en `seed_config`.

## Pruebas (criterios EARS → tests)
- [ ] T6 — test CA-1: convocatorias mismo tipo+carrera+ventana → un grupo.
- [ ] T7 — test CA-2: el digest muestra representante + "y N más".
- [ ] T8 — test CA-3: sin similares → entrada individual.
- [ ] T9 — test CA-4: el feed sigue mostrando todas las convocatorias.

## Cierre
- [ ] Sin migraciones (no cambia el modelo).
- [ ] Agrupa sin ocultar ni borrar.
- [ ] Definition of Done de la constitución cumplido.
