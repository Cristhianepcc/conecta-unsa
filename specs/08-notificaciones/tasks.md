# Tareas — 08 Notificaciones

## Implementación
- [ ] T1 — Modelos Notificacion, ResumenSemanalLog + migraciones.
- [ ] T2 — `construir_resumen(egresado)` (usa matching.feed + silenciadas + frecuencia).
- [ ] T3 — Plantilla HTML del resumen semanal.
- [ ] T4 — Integración Resend (env vars) + backend consola en local.
- [ ] T5 — Comando `enviar_resumenes` (para cron de Railway).
- [ ] T6 — `notificar()` + campana in-app (header dashboard).

## Pruebas
- [ ] T7 — test CA-1: un solo correo con las pertinentes.
- [ ] T8 — test CA-3: sin novedades → no envía.
- [ ] T9 — test CA-4: respeta silenciadas.
- [ ] T10 — test CA-5: evento → notificación in-app.

## Cierre
- [ ] DoD cumplido.
