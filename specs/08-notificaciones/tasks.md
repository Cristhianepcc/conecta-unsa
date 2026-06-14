# Tareas — 08 Notificaciones

## Implementación
- [x] T1 — Modelos Notificacion, ResumenSemanalLog + migraciones.
- [x] T2 — `construir_resumen(egresado)` (usa matching.feed + silenciadas + frecuencia; solo novedades).
- [x] T3 — Plantilla HTML + texto del resumen semanal.
- [x] T4 — Integración Resend vía SMTP (env) + backend consola en local + outbox en tests.
- [x] T5 — Comando `enviar_resumenes` (para cron de Railway).
- [x] T6 — `notificar()` + campana in-app (context processor + `_campana.html` en el header).

## Pruebas
- [x] T7 — test CA-1/CA-2: un solo correo con las pertinentes, al remitente configurado.
- [x] T8 — test CA-3: sin novedades → no envía.
- [x] T9 — test CA-4: respeta silenciadas (+ frecuencia «ninguna»).
- [x] T10 — test CA-5: evento → notificación in-app (+ observación notifica al reclutador, CA-6 de 06).
- [x] CA-6: ResumenSemanalLog registra cada envío.

## Cierre
- [x] DoD cumplido — 9 tests EARS verdes.

> Notas:
> - Resend por SMTP (smtp.resend.com) cuando hay RESEND_API_KEY; consola en dev. CA-2 vía
>   DEFAULT_FROM_EMAIL. El cron de Railway ejecuta `manage.py enviar_resumenes` semanalmente.
> - El hook `notificar_observacion_convocatoria` de 06 ya queda conectado (CA-6 de 06 completo).
> - «Novedades» = convocatorias del feed no incluidas en un ResumenSemanalLog previo (anti-reenvío).
