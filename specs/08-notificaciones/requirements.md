# Requisitos — 08 Notificaciones

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../notificaciones.md`](../../notificaciones.md).

## Objetivo
Reducir saturación con un **resumen semanal consolidado** por correo (Resend) y un centro de
notificaciones in-app (campana).

## Alcance
- **Incluye:** digest semanal (cron + Resend), notificaciones in-app, plantilla de correo.
- **No incluye:** SMTP institucional real (futuro), preferencias (en `07`).

## Historias de usuario
- **HU-1:** Como egresado, quiero un solo correo semanal con lo pertinente, no muchos sueltos.
- **HU-2:** Como egresado, quiero ver avisos en una campana dentro de la plataforma.
- **HU-3:** Como empresa, quiero recibir aviso cuando mi convocatoria es observada.

## Criterios de aceptación (EARS)
- **CA-1:** Cuando corre el cron semanal, el sistema debe armar **un solo correo** por egresado con sus convocatorias pertinentes (vía `matching.feed`).
- **CA-2:** El sistema debe enviar el correo con **Resend** desde el remitente configurado.
- **CA-3:** Si un egresado no tiene convocatorias nuevas, entonces el sistema **no** debe enviarle correo.
- **CA-4:** El sistema debe respetar la **frecuencia** y categorías silenciadas del perfil.
- **CA-5:** Cuando ocurre un evento relevante (nueva pertinente, observada, fecha límite), el sistema debe crear una **notificación in-app**.
- **CA-6:** El sistema debe registrar cada envío (log) para auditoría.

## Dependencias
- `05-matching` (feed), `07-perfil` (preferencias), `00` (Resend env).

## Notas
- Sin Celery/Redis: cron de Railway + `manage.py`. Secretos en env (NFR-SEC-2).
