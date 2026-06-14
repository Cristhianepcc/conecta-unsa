# Requisitos — 06 Flujo Admin

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../flujo-admin.md`](../../flujo-admin.md).

## Objetivo
Gestionar el ciclo de vida de las convocatorias con mínima carga: estados, alertas automáticas,
detección de duplicados y semáforo de confianza (auto-publicar vs revisión humana).

## Alcance
- **Incluye:** transiciones de estado, alertas, duplicados (pg_trgm), semáforo, caducidad automática.
- **No incluye:** la UI del panel (`12`), la difusión/matching (`05`).

## Historias de usuario
- **HU-1:** Como administrativo, quiero ver alertas sobre convocatorias pendientes para revisar rápido.
- **HU-2:** Como administrativo, quiero que las buenas convocatorias de empresas verificadas se publiquen solas.
- **HU-3:** Como administrativo, quiero devolver una convocatoria observada con un comentario.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe mover una convocatoria entre estados válidos (borrador→pendiente→publicada/observada/rechazada; →caducada).
- **CA-2:** Cuando entra una convocatoria, el sistema debe calcular alertas: duplicado, incompleta, baja transparencia, exceso de difusión.
- **CA-3:** El sistema debe marcar **posible duplicado** si misma empresa + título similar (pg_trgm) + ≤30 días.
- **CA-4:** Cuando una empresa **verificada** publica una convocatoria **sin alertas y 🟢**, entonces el sistema debe **auto-publicarla**.
- **CA-5:** Si la empresa es nueva o hay alertas, entonces el sistema debe dejar la convocatoria en **pendiente** para revisión humana.
- **CA-6:** Cuando el admin **observa** una convocatoria, el sistema debe registrar el comentario y notificar a la empresa.
- **CA-7:** Mientras una convocatoria pase su fecha límite, el sistema debe marcarla **caducada** (automático).

## Dependencias
- `04-convocatorias`, `03-empresas`, `00` (pg_trgm, parámetros).

## Notas
- Duplicados sin IA (pg_trgm). Semáforo = "priorización asistida".
