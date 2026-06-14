# Diseño — 12 Panel Admin

## App
`convocatorias` / `core` (vistas a medida) + Django Admin.

## Vistas / rutas
| Ruta | Descripción |
|---|---|
| `/admin-panel` | bandeja + métricas (template a medida) |
| `/admin-panel/convocatoria/<id>` | revisar: aprobar/observar/rechazar |
| `/admin` | Django Admin (CRUD, config-as-data, empresas referenciales) |

## UI (según `Dashboard administrativo.png`)
- Tarjetas superiores: recibidas, validadas, pendientes, duplicados, índice de transparencia.
- Bandeja con badges de **alerta** (🔴 duplicado, 🟡 incompleta/baja transp., 🟠 exceso) y semáforo.
- Paneles: clasificación por categoría, métricas de difusión, control de frecuencia, reportes.

## Acceso
- `admin_required` (rol por `AdminAllowlist`) → CA-6.

## Decisiones
- Lo visual e impactante (bandeja, métricas) = template a medida; el CRUD pesado y la
  configuración (parámetros, pesos, elegibilidad, taxonomía) = Django Admin (gratis).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,3 | bandeja + alertas (de `06`) + test |
| CA-2 | acciones aprobar/observar/rechazar (de `06`) + test |
| CA-4 | métricas reales + test |
| CA-5 | Django Admin |
| CA-6 | `admin_required` + test |
