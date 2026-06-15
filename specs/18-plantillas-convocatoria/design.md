# Diseño — 18 Plantillas reutilizables de convocatoria

> Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
`convocatorias` (modelo + form). Reusa publicar de `empresas`.

## Modelos (sync gate en modelo-datos.md)
```
PlantillaConvocatoria
  ├─ nombre        CharField              # "Práctica preprofesional"
  ├─ tipo          CharField (choices = TIPOS_CONVOCATORIA)
  ├─ activa        BooleanField (default True)
  ├─ valores       JSONField              # {campo: valor} para pre-llenar el form
  └─ creada_en     DateTimeField
```
- `valores` guarda solo campos del `ConvocatoriaForm` (título sugerido, descripción, modalidad,
  niveles 2/3). Validado contra los nombres de campo del form al guardar (admin).

## Servicios (lógica de negocio)
- `plantillas_activas()` → `PlantillaConvocatoria.objects.filter(activa=True)`.
- `initial_desde_plantilla(plantilla)` → dict `initial` filtrado a campos válidos del form.

## Vistas / rutas
| Ruta | Método | Rol | Descripción |
|---|---|---|---|
| `/empresas/publicar/` | GET `?plantilla=<id>` | empresa | instancia `ConvocatoriaForm(initial=...)` |
| `/empresas/publicar/` | GET | empresa | muestra selector de plantilla (paso 0) |

## Templates / UI
- Paso 0 en publicar: tarjetas/selector de plantillas activas + opción "Empezar en blanco".
- Al elegir, recarga el form con `?plantilla=<id>` (server-side `initial`) → simple y sin JS pesado.
- Banner sutil "Partiste de la plantilla *X* — edita lo que necesites" (refuerza CA-3).

## Configuración (config-as-data)
- Alta/edición de plantillas en Django Admin (MVP) o panel admin (`12`).
- Seed de 3-4 plantillas base (práctica, empleo, voluntariado, beca/servicio).

## Decisiones de diseño
- Pre-llenado **server-side** vía `initial` (no sobrescribe lo que la empresa edite) → CA-2/CA-3.
- `valores` como JSON (no columnas espejo) → flexible y sin migraciones por cada campo nuevo.
- Plantillas **institucionales** (no por empresa) en v1 → menor superficie, mayor estandarización.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | modelo `PlantillaConvocatoria` + admin |
| CA-2 | `initial_desde_plantilla` + vista publicar + test |
| CA-3 | `initial` (no fuerza) + test de edición |
| CA-4 | publicar sin `?plantilla` (form en blanco) + test |
