# Tareas — 10 Dashboard Estudiante/Egresado

## Implementación
- [x] T1 — Vista `/dashboard` con `matching.feed` (elegibles ordenadas + motivo).
- [x] T2 — Tarjeta de convocatoria reutilizable (badge transparencia + motivo).
- [x] T3 — Detalle `/convocatorias/<id>` + "postular" (redirige al medio externo) + registra vista.
- [x] T4 — Modelo InteraccionConvocatoria (vista/guardada); `/guardadas`, `/historial`.
- [x] T5 — Bloque resumen semanal + campana (de `08`) en el dashboard.
- [x] T6 — Acceso a preferencias (`/perfil`, reusa `07`).

## Pruebas
- [x] T7 — test CA-1: el feed solo muestra elegibles para su carrera.
- [x] T8 — test CA-3: "postular" redirige y registra vista (+ detalle registra vista).
- [x] T9 — test CA-4: guardar (toggle) y ver guardadas/historial.
- [x] CA-2 (transparencia/motivo en tarjeta).

## Cierre
- [x] DoD cumplido — 6 tests EARS verdes. AA: tarjetas semánticas, foco, contraste.

> Nota: "postular" = redirección al medio externo (mailto/URL); la plataforma no gestiona la
> selección. La vista registrada alimenta `matching.alcance` y el panel admin.
