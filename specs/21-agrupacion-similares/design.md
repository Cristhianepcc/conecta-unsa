# Diseño — 21 Agrupación de convocatorias similares

> Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
`convocatorias` (servicio de agrupación) usado por `notificaciones` (digest) y `core` (bandeja).
Sin app ni modelo nuevos.

## Modelos
Sin cambios. Agrupa sobre:
```
Convocatoria.tipo / carreras_objetivo / creada_en      # ya existe
ParametroLegal.agrupacion_ventana_dias                  # config-as-data
```

## Servicios (lógica de negocio)
```
# apps/convocatorias/agrupacion.py (nuevo)
agrupar_similares(convocatorias) -> list[Grupo]
  # Grupo = {representante: Convocatoria, similares: [Convocatoria], clave: (tipo, carrera)}
  # Regla: misma `tipo` + intersección no vacía de `carreras_objetivo`
  #        + |creada_en| dentro de la ventana. Unión por componentes conexos simples.
```
- Determinista y explicable: la "clave" del grupo es legible (tipo + carrera compartida).
- Reusable: el digest le pasa `construir_resumen(usuario)`; la bandeja admin le pasa las pendientes.

## Vistas / rutas
| Ruta | Método | Rol | Descripción |
|---|---|---|---|
| (digest, sin ruta) | — | egresado | `resumen_email` renderiza grupos: representante + "y N más" |
| `/panel-admin/` | GET | admin | toggle "agrupar similares" en la bandeja (opcional) |

## Templates / UI
- `resumen_email.html/.txt`: por grupo, mostrar el representante (mayor afinidad/transparencia) y
  "y N convocatorias similares" con enlace a verlas.
- Bandeja admin: encabezado de grupo plegable (no oculta filas; las agrupa visualmente).

## Configuración (config-as-data)
- `ParametroLegal.agrupacion_ventana_dias` (entero, default 14).

## Decisiones de diseño
- **Agrupar, no fusionar** → nada se borra/oculta; el feed sigue mostrando todo (CA-4, auditabilidad).
- Representante = el de mayor `transparencia_pct` (o afinidad en el digest) → premia calidad.
- Reglas simples (tipo + carrera + ventana), sin embeddings → coherente con "sin IA".

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | `agrupar_similares` (tipo + carrera + ventana) + test |
| CA-2 | render de grupos en `resumen_email` + test |
| CA-3 | singleton → grupo de 1 mostrado individual + test |
| CA-4 | feed/detalle intactos (agrupación solo en presentación) + test |
