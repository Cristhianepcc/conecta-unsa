# Requisitos — 10 Dashboard Estudiante/Egresado

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../paginas.md`](../../paginas.md), [`../../matching.md`](../../matching.md).

## Objetivo
Experiencia del egresado: feed pertinente y ordenado, resumen semanal, preferencias, transparencia
y campana — con baja saturación.

## Alcance
- **Incluye:** feed (matching), tarjetas de convocatoria, resumen semanal, preferencias, historial de vistas/guardados, campana, transparencia visible.
- **No incluye:** postulación (redirige al link externo; la plataforma no gestiona selección).

## Historias de usuario
- **HU-1:** Como egresado, quiero ver oportunidades para mí, ordenadas por afinidad y con el motivo.
- **HU-2:** Como egresado, quiero guardar/ver historial y configurar preferencias.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe mostrar el **feed** de `matching.feed(usuario)` (elegibles + ordenadas).
- **CA-2:** Cada convocatoria debe mostrar su **% de transparencia** (semáforo) y, si aplica, el **motivo** de recomendación.
- **CA-3:** Cuando el egresado pulsa "postular", el sistema debe **redirigir al medio externo** (no gestiona la postulación) y registrar la **vista**.
- **CA-4:** El sistema debe permitir **guardar** convocatorias y ver **historial** de vistas/guardadas.
- **CA-5:** El sistema debe mostrar el **resumen semanal** (vista de lo que llega por correo) y la **campana** de avisos.
- **CA-6:** El sistema debe permitir editar **preferencias** (de `07`).

## Dependencias
- `05-matching`, `07-perfil`, `08-notificaciones`, `04-convocatorias`.

## Notas
- Sin feed social ni perfiles públicos (NO red social).
