# Requisitos — 13 Vigencia en feed y digest

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../06-flujo-admin/requirements.md`](../06-flujo-admin/requirements.md), [`../08-notificaciones/requirements.md`](../08-notificaciones/requirements.md).

## Objetivo
Garantizar que el egresado **nunca** vea ni reciba convocatorias **vencidas**, aunque el
cron de caducidad no haya corrido todavía. Cerrar la dependencia silenciosa entre la
vigencia y la ejecución del cron.

## Contexto (estado actual del código)
- La **landing** (`core/services.py:_convocatorias_activas`) y el **dashboard de empresa**
  (`empresas/services.py`) ya filtran por `fecha_limite >= hoy`. ✅
- El **feed del egresado** y el **resumen semanal** usan `matching.feed()` →
  `convocatorias_publicadas()` (`apps/matching/services.py:80`), que filtra **solo**
  `estado=ESTADO_PUBLICADA`, **sin** mirar `fecha_limite`. ❌
- Existe `flujo.caducar_vencidas()` y el comando `caducar_vencidas`, pero `railway.json`
  **no programa ningún cron**. ❌

## Alcance
- **Incluye:** filtrar vencidas en el origen del feed; documentar/cablear los dos cron de
  Railway (`caducar_vencidas` diario, `enviar_resumenes` semanal).
- **No incluye:** cambios de modelo; rediseño de la máquina de estados (ya existe en `06`).

## Historias de usuario
- **HU-1:** Como egresado, no quiero ver en mi feed convocatorias cuyo plazo ya venció.
- **HU-2:** Como egresado, no quiero recibir en mi correo semanal convocatorias vencidas.
- **HU-3:** Como Bolsa de Trabajo, quiero que las vencidas pasen a `caducada`
  automáticamente cada día sin intervención manual.

## Criterios de aceptación (EARS)
- **CA-1:** El feed del egresado (`matching.feed`) **no debe** incluir convocatorias con
  `fecha_limite < hoy`, aunque sigan en estado `publicada`.
- **CA-2:** Cuando se arma el resumen semanal, el sistema **no debe** incluir convocatorias
  vencidas (hereda de CA-1 vía `matching.feed`).
- **CA-3:** Una convocatoria **sin** `fecha_limite` (null) debe seguir apareciendo (no expira).
- **CA-4:** El comando `caducar_vencidas` debe quedar **programado como cron diario** en
  Railway; `enviar_resumenes` como **cron semanal**.
- **CA-5:** El cambio **no debe** afectar landing ni dashboard de empresa (ya correctos).

## Dependencias
- `05-matching` (dueño de `convocatorias_publicadas`), `06-flujo-admin` (`caducar_vencidas`),
  `08-notificaciones` (digest), `00-fundacion` (`railway.json`).

## Notas
- Sin Celery/Redis: cron de Railway + `manage.py` (NFR de la constitución).
- El filtro por fecha es defensa en profundidad: aunque el cron falle, el egresado queda
  protegido.
