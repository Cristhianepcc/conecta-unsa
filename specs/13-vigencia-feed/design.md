# Diseño — 13 Vigencia en feed y digest

## App
`matching` (cambio principal) · `00-fundacion` (`railway.json`)

## Cambio central
```
# apps/matching/services.py
def convocatorias_publicadas():
    hoy = timezone.localdate()
    return (
        Convocatoria.objects
        .filter(estado=ESTADO_PUBLICADA)
        .filter(Q(fecha_limite__gte=hoy) | Q(fecha_limite__isnull=True))  # ← nuevo
    )
```
- Un único punto de cambio: **todas** las capas (`elegibles_por_estado`,
  `elegibles_por_carrera`, `feed`, `alcance`, `construir_resumen`) parten de aquí, así que
  el filtro se propaga sin tocarlas.
- Reusa el mismo predicado que ya usan `core/services.py:_convocatorias_activas` y
  `empresas/services.py` → consistencia entre las tres superficies.

## Cron (Railway)
- `railway.json` no admite schedules; los cron de Railway se definen como **servicios
  cron** en el dashboard apuntando al mismo deploy:
  - `python manage.py caducar_vencidas` — diario (ej. 03:00).
  - `python manage.py enviar_resumenes` — semanal (ej. lunes 08:00).
- Documentar en `ENTREGA.md` el schedule exacto (ya menciona los comandos; falta el cron).

## UI
- Sin cambios visibles. El egresado simplemente deja de ver/recibir vencidas.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,2,3 | filtro en `convocatorias_publicadas` + tests |
| CA-4 | cron Railway + nota en `ENTREGA.md` |
| CA-5 | landing/empresa ya usan su propio filtro; no se tocan |

## Riesgos
- Si alguna vista del egresado consulta `Convocatoria.objects` directo (sin pasar por
  `matching`), debe migrarse a `convocatorias_publicadas()`. Auditar `detalle`/`postular`.
