# Requisitos — 15 Empleabilidad (eventos y talleres segmentados)

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../08-notificaciones/requirements.md`](../08-notificaciones/requirements.md), [`../01-taxonomia/requirements.md`](../01-taxonomia/requirements.md).

## Objetivo
Cubrir el insight 4 del desafío ("acompañamiento real en la transición": orientación,
talleres, empleabilidad), hoy casi ausente. Permitir a la Bolsa de Trabajo publicar
**eventos/talleres** y difundirlos **segmentados por carrera**, reusando la infraestructura
de notificaciones existente.

## Contexto (estado actual del código)
- Ya existe un sistema de **comunicados institucionales**: comando `mensaje_institucional`,
  bandeja `institucionales` (`notificaciones/views.py:22`), `TIPO_GENERAL` y campana. ✅
- Pero `mensaje_institucional` se envía a **todos** los egresados, sin segmentar. ❌
- No existe modelo de evento/taller (fecha, cupo, carreras objetivo). ❌

## Alcance
- **Incluye:** modelo `Evento` (taller/charla/feria), listado para egresados, difusión
  segmentada por carrera vía la campana/comunicados existentes.
- **No incluye:** inscripción con control de cupo en tiempo real, pasarela de pago,
  videoconferencia. (Enlace externo a inscripción, como las convocatorias.)

## Historias de usuario
- **HU-1:** Como Bolsa de Trabajo, quiero publicar un taller de empleabilidad dirigido a
  ciertas carreras y que solo esos egresados reciban el aviso.
- **HU-2:** Como egresado, quiero ver los talleres/eventos pertinentes a mi carrera y un
  enlace para inscribirme.
- **HU-3:** Como universidad, quiero que el canal institucional ofrezca acompañamiento, no
  solo convocatorias de empleo.

## Criterios de aceptación (EARS)
- **CA-1:** Un admin debe poder crear un `Evento` con título, descripción, fecha, modalidad,
  enlace de inscripción y **carreras objetivo** (M2M).
- **CA-2:** El egresado debe ver, en una sección de empleabilidad, los eventos **futuros**
  cuyas carreras objetivo incluyan su carrera (o sin carrera objetivo = abiertos a todos).
- **CA-3:** Cuando se publica un evento segmentado, el sistema debe notificar in-app **solo**
  a los egresados de esas carreras (reusando `notificar` / `TIPO_GENERAL`).
- **CA-4:** Eventos **pasados** no deben listarse en la sección activa del egresado.
- **CA-5:** El evento debe ofrecer el enlace de inscripción **externo** (la plataforma no
  gestiona la inscripción).

## Dependencias
- `01-taxonomia` (Carrera), `08-notificaciones` (campana/`notificar`),
  `12-panel-admin` o Django admin (alta de eventos).

## Notas
- **Sync gate (modelo-datos):** añade el modelo `Evento`; proponer en `modelo-datos.md`
  antes de implementar (modelo congelado por la constitución).
- Reusa al máximo lo existente: la difusión segmentada es `notificar()` filtrando por
  `PerfilTalento.carrera`, no infraestructura nueva.
- App nueva sugerida `empleabilidad` (un solo dueño) para no mezclar con `notificaciones`.
