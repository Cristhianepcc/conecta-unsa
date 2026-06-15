# Tareas — 13 Vigencia en feed y digest

## Implementación
- [x] T1 — Filtro `fecha_limite >= hoy | isnull` en
  `apps/matching/services.py:convocatorias_publicadas()`.
- [x] T2 — `postular` (`convocatorias/views.py`) guarda con `conv.activa`: no redirige a
  vencidas aunque el cron no las haya caducado.
- [x] T3 — `ENTREGA.md` documenta el schedule de ambos cron (caducidad diaria `0 3 * * *`,
  resumen semanal `0 8 * * 1`) y aclara que la vigencia ya está blindada por código.

## Pruebas
- [x] T4 — test CA-1: `publicada` con `fecha_limite` ayer → **no** aparece en `feed`.
- [x] T5 — test CA-2: el resumen (`construir_resumen`) excluye la vencida.
- [x] T6 — test CA-3: `fecha_limite=None` sí aparece. (+ `convocatorias_publicadas()==0`.)
- [x] T7 — no regresión: `core`(22) y `empresas`(16) siguen verdes.

## Cierre
- [x] DoD — tests EARS verdes (matching 14, incl. 4 nuevos). Cron documentado; cableado en
  el dashboard de Railway queda como paso de despliegue.

> Nota: cambio de 1 línea de lógica + cron. Alto impacto, bajo esfuerzo. Es la defensa en
> profundidad para que la vigencia no dependa solo de que el cron haya corrido.
