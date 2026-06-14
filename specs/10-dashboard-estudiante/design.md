# Diseño — 10 Dashboard Estudiante/Egresado

## App
`usuarios` / `convocatorias` (vistas) + templates.

## Modelos (añade)
```
InteraccionConvocatoria → usuario · convocatoria · tipo(vista|guardada) · creado
```

## Vistas / rutas
| Ruta | Descripción |
|---|---|
| `/dashboard` | feed pertinente + resumen + campana |
| `/convocatoria/<id>` | detalle + botón "postular" (redirige) |
| `/guardadas` `/historial` | guardadas y vistas |
| `/preferencias` | edición (reusa `07`) |

## UI (según mockup)
- Tarjetas de convocatoria con badge de transparencia y "recomendado porque…".
- Bloques: resumen semanal, categorías, preferencias, transparencia, mensaje institucional.
- Campana 🔔 (de `08`). Copy "estudiantes y egresados". Tailwind/Alpine, AA.

## Decisiones
- "Postular" = link externo (la plataforma no gestiona selección — propuesta).
- Registrar `vista` alimenta métricas de alcance (`matching.alcance` / panel admin).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,2 | feed + tarjetas + test |
| CA-3 | redirect + registro de vista + test |
| CA-4 | InteraccionConvocatoria + test |
| CA-5 | resumen + campana |
| CA-6 | preferencias (07) |
