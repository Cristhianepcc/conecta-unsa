# Diseño — 11 Dashboard Empresa

## App
`empresas` / `convocatorias` (vistas) + templates.

## Vistas / rutas
| Ruta | Descripción |
|---|---|
| `/empresa` | inicio: métricas propias + "Mis convocatorias" |
| `/empresa/publicar` | form dinámico 3 bloques (`04`) |
| `/empresa/convocatoria/<id>/editar` | editar / corregir observada |
| `/empresa/perfil` | datos de empresa |

## UI (según `dashboard empresa.png`)
- Sidebar (Inicio, Mis convocatorias, Publicar, Borradores, Estadísticas, Mensajes, Perfil, Guías).
- Tarjetas de métricas (activas, alcance, vistas, difundidas) — **calculadas**.
- Tabla "Mis convocatorias": tabs (Todas/Activas/En revisión/Publicadas/Borradores/Archivadas)
  + columnas estado, completitud, fecha, alcance, acciones.
- Bloque "Estado de tu empresa" (Verificada + indicadores) y "Transparencia y estandarización".
- **Nueva vista (gap):** "Requiere corrección" para convocatorias **observadas** (comentario + editar).
- **Estado no verificada:** dashboard limitado con aviso "tu cuenta está en verificación".

## Mapeo de estados (UI ↔ modelo)
- "En revisión" = pendiente · "Activa" = publicada vigente · "Archivada" = caducada · + "Observada".

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,5 | lista + métricas calculadas + test |
| CA-2 | form de `04` |
| CA-3 | guard no verificada + test |
| CA-4 | vista corregir observada + test |
| CA-6 | bloque estado + guías |
