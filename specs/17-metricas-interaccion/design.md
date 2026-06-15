# Diseño — 17 Métricas de interacción y alcance

> Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
`convocatorias` (servicio de métricas) + `core` (panel). Sin app nueva, sin modelo nuevo.

## Modelos
Sin cambios. Se agrega sobre:
```
InteraccionConvocatoria (vista | guardada)   # ya existe
Convocatoria.carreras_objetivo               # para alcance (Gate 2)
PerfilTalento.estado_academico / carrera     # para alcance (Gate 1/2)
```

## Servicios (lógica de negocio)
```
# apps/convocatorias/metricas.py (nuevo)
metricas_interaccion()      → {
    vistas: int, guardados: int,
    con_interaccion_pct: float,            # % de publicadas con ≥1 interacción
    top: [ {conv, vistas, guardados, total} ]   # top N por total
}
alcance_pertinente(conv)    → int          # nº de PerfilTalento que pasan Gate 1+2 para esa conv
```
- `vistas/guardados`: `InteraccionConvocatoria.objects.filter(tipo=...).count()`.
- `top`: `annotate(Count('interacciones'))order_by('-...')[:N]`.
- `alcance_pertinente`: reusa la lógica de gates de `matching` aplicada al universo de perfiles
  (no envía nada; solo cuenta). N configurable por `ParametroLegal` (`top_convocatorias`, default 5).

## Vistas / rutas
| Ruta | Método | Rol | Descripción |
|---|---|---|---|
| `/panel-admin/` | GET | admin | añade `metricas_interaccion()` al contexto y un bloque en la plantilla |

## Templates / UI
- Nueva fila de tarjetas en el panel: **Vistas**, **Guardados**, **% con interacción**.
- Tabla compacta "Top convocatorias por interacción" (título · empresa · vistas · guardados).
- Estado vacío: ceros y mensaje "Aún sin interacciones registradas".

## Configuración (config-as-data)
- `ParametroLegal.top_convocatorias` (entero, default 5).

## Decisiones de diseño
- Cálculo **on-read** (sin tabla de agregados) → simple y suficiente para el volumen del MVP;
  si crece, se materializa luego.
- `alcance_pertinente` se ofrece como servicio reutilizable (también útil en el detalle admin).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | `metricas_interaccion.vistas/guardados` + test |
| CA-2 | `metricas_interaccion.top` + test |
| CA-3 | `alcance_pertinente` (gates) + test |
| CA-4 | estado vacío (ceros) + test |
