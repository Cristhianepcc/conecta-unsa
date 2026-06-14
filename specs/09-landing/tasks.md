# Tareas — 09 Landing pública

## Implementación
- [x] T1 — Vista `/` + base con nav y footer institucional (privacidad/términos/contacto).
- [x] T2 — Hero con 2 puertas (egresado/empresa) + CTAs jerarquizadas (1 primaria + 1 secundaria).
- [x] T3 — "Cómo funciona" (3 pasos) — reemplaza vanity stats.
- [x] T4 — Categorías desde la taxonomía real con conteos reales.
- [x] T5 — Sección transparencia con semáforo 🟢🟡🔴 + métricas honestas.
- [x] T6 — Páginas `/privacidad`, `/terminos`, `/como-funciona` (base legal Ley 29733/26772).
- [x] T7 — Helpers `metricas_landing()` y `categorias_con_conteo()` (calculados de BD).

## Pruebas
- [x] T8 — test CA-1: las métricas vienen de la BD y cambian con los datos (no constantes).
- [x] T9 — test CA-3: categorías = taxonomía real (3 áreas).
- [x] CA-2 (2 puertas), CA-4 (semáforo), CA-5 (footer institucional).

## Cierre
- [x] DoD cumplido — 7 tests EARS verdes. Responsive + AA (contraste granate, foco, saltar al contenido).

> Nota: nada de vanity metrics; convocatorias activas = publicadas y vigentes; índice de
> transparencia = promedio real de `transparencia_pct` de las activas.
