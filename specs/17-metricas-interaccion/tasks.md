# Tareas — 17 Métricas de interacción y alcance

> Deriva de `design.md`.

## Implementación
- [ ] T1 — `apps/convocatorias/metricas.py`: `metricas_interaccion()` (vistas, guardados, %, top).
- [ ] T2 — `alcance_pertinente(conv)` reusando los gates de `matching`.
- [ ] T3 — Inyectar `metricas_interaccion()` en `core.views.panel_admin`.
- [ ] T4 — Bloque de métricas + tabla "Top convocatorias" en la plantilla del panel.

## Datos / seed
- [ ] T5 — Parámetro `top_convocatorias` en `seed_config` (default 5).

## Pruebas (criterios EARS → tests)
- [ ] T6 — test CA-1: cuenta vistas y guardados correctamente.
- [ ] T7 — test CA-2: el top ordena por total de interacciones.
- [ ] T8 — test CA-3: `alcance_pertinente` cuenta solo egresados elegibles (Gate 1+2).
- [ ] T9 — test CA-4: sin interacciones → ceros sin error.

## Cierre
- [ ] Sin migraciones (no cambia el modelo).
- [ ] Métricas agregadas, sin datos personales.
- [ ] Definition of Done de la constitución cumplido.
