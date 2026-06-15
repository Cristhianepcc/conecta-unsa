# Diseño — 19 Monitoreo de volumen por empresa

> Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
`convocatorias` (`flujo.py`) + `core` (panel). Sin app ni modelo nuevos.

## Modelos
Sin cambios. Cuenta sobre:
```
Convocatoria.empresa / creada_en / estado     # ya existe
ParametroLegal                                  # umbral y ventana (config-as-data)
```

## Servicios (lógica de negocio)
```
# apps/convocatorias/flujo.py (ampliar)
volumen_reciente(empresa, dias) -> int          # nº de convocatorias en la ventana
hay_exceso_difusion(conv) -> bool               # volumen_reciente(conv.empresa, ventana) > umbral
```
- Integrar en `calcular_alertas(conv)`: si `hay_exceso_difusion(conv)` → añadir alerta
  `"exceso_difusion"` al set existente → eleva el riesgo en la bandeja (reusa el cálculo actual).

## Vistas / rutas
| Ruta | Método | Rol | Descripción |
|---|---|---|---|
| `/panel-admin/` | GET | admin | la alerta aparece en la bandeja como una más (sin ruta nueva) |
| `/panel-admin/convocatoria/<id>/` | GET | admin | muestra "Esta empresa publicó N en los últimos D días" |

## Templates / UI
- Chip/etiqueta de alerta "Exceso de difusión" en la fila de la bandeja (reusa el patrón de alertas).
- En el detalle de revisión: línea informativa con el conteo y la ventana.

## Configuración (config-as-data)
- `ParametroLegal.exceso_ventana_dias` (entero, default 7).
- `ParametroLegal.exceso_umbral` (entero, default 5).

## Decisiones de diseño
- **Alerta, no bloqueo** → respeta la proporcionalidad de la propuesta; el admin decide.
- Reutiliza el pipeline de `calcular_alertas`/riesgo ya existente → mínima superficie nueva.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | `volumen_reciente` + test |
| CA-2 | `hay_exceso_difusion` integrado en `calcular_alertas` + test |
| CA-3 | bajo umbral → sin alerta + test |
| CA-4 | `ParametroLegal` (umbral/ventana) + seed |
