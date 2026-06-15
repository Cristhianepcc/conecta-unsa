# Tareas — 19 Monitoreo de volumen por empresa

> Deriva de `design.md`.

## Implementación
- [ ] T1 — `flujo.volumen_reciente(empresa, dias)`.
- [ ] T2 — `flujo.hay_exceso_difusion(conv)` usando umbral/ventana de `ParametroLegal`.
- [ ] T3 — Integrar la alerta `exceso_difusion` en `calcular_alertas`.
- [ ] T4 — Mostrar el dato en la bandeja y en el detalle de revisión del panel admin.

## Datos / seed
- [ ] T5 — Parámetros `exceso_ventana_dias` (7) y `exceso_umbral` (5) en `seed_config`.

## Pruebas (criterios EARS → tests)
- [ ] T6 — test CA-1: `volumen_reciente` cuenta dentro de la ventana.
- [ ] T7 — test CA-2: superar el umbral genera alerta y eleva el riesgo.
- [ ] T8 — test CA-3: bajo el umbral no hay alerta ni cambio de flujo.

## Cierre
- [ ] Sin migraciones (no cambia el modelo).
- [ ] Monitorea sin bloquear.
- [ ] Definition of Done de la constitución cumplido.
