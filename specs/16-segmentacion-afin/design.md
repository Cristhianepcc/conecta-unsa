# Diseño — 16 Segmentación por carreras afines

> Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
`convocatorias` (form) + `taxonomia` (expansión). Sin app nueva, sin modelo nuevo.

## Modelos
Sin cambios. Se reutiliza:
```
Convocatoria.carreras_objetivo  M2M(Carrera)      # destino final ya existente
GrupoAfin                                          # ya existe (taxonomia)
  ├─ nombre  : CharField
  └─ carreras → M2M(Carrera)
```

## Servicios (lógica de negocio)
- `taxonomia.services.carreras_de(seleccion)` → ya expande `GrupoAfin` → carreras (reusar).
- Nuevo helper en el form: `_expandir_grupos(grupos) -> set[Carrera]` = unión de `carreras_de`.

## Vistas / rutas
| Ruta | Método | Rol | Descripción |
|---|---|---|---|
| `/empresas/publicar/` | POST | empresa | añade campo no-modelo `grupos_afines` (MultipleChoice) |
| `/empresas/<id>/editar/` | POST | empresa | idem |

## Form
- `ConvocatoriaForm` gana un campo **no-modelo** `grupos_afines = ModelMultipleChoiceField(GrupoAfin.objects.all(), required=False)`.
- En `save()`: tras guardar la instancia y los M2M, hacer
  `obj.carreras_objetivo.add(*_expandir_grupos(cleaned["grupos_afines"]))`
  (unión con las carreras marcadas a mano → CA-3, sin duplicar por ser `add` sobre M2M).

## Templates / UI
- En `_form.html`, bloque "Dirigida a": multiselect/чips de grupos afines **encima** del selector
  de carreras, con ayuda: "Elige un grupo (ej. *Administración o afines*) o carreras sueltas".
- Estado vacío: si no marca nada, la convocatoria queda abierta a todas (comportamiento actual).

## Configuración (config-as-data)
- Los `GrupoAfin` y sus miembros se editan en Django Admin / panel (ya soportado por el modelo).

## Decisiones de diseño
- **Expandir al guardar** (no en tiempo de feed) → la convocatoria conserva su audiencia exacta
  aunque el grupo cambie después (CA-4, auditabilidad). El Gate 2 no necesita cambios.
- No se añade campo de modelo → cero migración, cero riesgo sobre el modelo congelado.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | `ConvocatoriaForm.save` + `carreras_de` + test |
| CA-2 | Gate 2 existente (`elegibles_por_carrera`) + test |
| CA-3 | `M2M.add(*union)` + test |
| CA-4 | expansión en guardado (snapshot) + test |
