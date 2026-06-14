# Requisitos — 12 Panel Admin

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: `paginas/Dashboard administrativo.png`, [`../../flujo-admin.md`](../../flujo-admin.md).

## Objetivo
Panel a medida para la Bolsa de Trabajo: bandeja de convocatorias con alertas, validación,
métricas y reducción de saturación — apoyado en Django Admin para CRUD pesado.

## Alcance
- **Incluye:** bandeja con alertas y semáforo, acciones (aprobar/observar/rechazar), métricas de difusión, control de empresas, reportes; Django Admin para config-as-data.
- **No incluye:** la lógica de flujo (`06`), matching (`05`).

## Historias de usuario
- **HU-1:** Como administrativo, quiero una bandeja priorizada por alertas para revisar rápido.
- **HU-2:** Como administrativo, quiero aprobar/observar/rechazar y activar empresas.
- **HU-3:** Como administrativo, quiero métricas y reportes institucionales.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe mostrar la **bandeja** de convocatorias con su estado, **alertas** y % transparencia.
- **CA-2:** El sistema debe permitir **aprobar / observar (con comentario) / rechazar** una convocatoria.
- **CA-3:** El sistema debe resaltar **duplicados** y mostrar su % de similitud.
- **CA-4:** El sistema debe mostrar **métricas** (difusión, alcance, completitud, índice de transparencia) **reales**.
- **CA-5:** El sistema debe permitir **activar/rechazar empresas** y **crear convocatorias/empresas referenciales** (vía Django Admin).
- **CA-6:** Mientras un usuario no sea admin (allowlist), el sistema debe **denegar** el acceso al panel.

## Dependencias
- `06-flujo-admin`, `03-empresas`, `04-convocatorias`, `05-matching`, `02` (rol admin).

## Notas
- Híbrido: template a medida + Django Admin (`/admin`).
