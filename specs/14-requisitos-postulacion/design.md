# Diseño — 14 Requisitos de postulación

## App
`convocatorias` (detalle/postular + servicio) · `usuarios` (solo lectura del perfil; modelo opcional en sync gate)

## Servicio nuevo
```
# apps/convocatorias/requisitos.py
def checklist_requisitos(conv, perfil) -> list[dict]:
    """Lista de requisitos evaluables de la convocatoria frente al perfil.
    Cada item: {etiqueta, requerido, estado}  donde estado ∈ {cumple, no_cumple, verifica}.
    No bloquea, no selecciona: solo informa.
    """
```
Reglas (solo si el campo está definido en la convocatoria):
```
ciclo_minimo         → si perfil.ciclo_actual conocido: cumple si ciclo_actual >= ciclo_minimo; si no: "verifica"
tiempo_egreso_meses  → si perfil.anio_egreso conocido: cumple si meses_desde_egreso <= tiempo_egreso_meses; si no: "verifica"
```

## Integración
- `convocatorias/views.py:detalle` → pasa `checklist = checklist_requisitos(conv, perfil)`
  al template.
- `convocatorias/views.py:postular` → si hay algún `no_cumple`, setea un mensaje
  no bloqueante (Django messages) antes del redirect; **no** impide postular (CA-3).

## Datos del perfil (sync gate — opcional, CA-5)
```
PerfilTalento + ciclo_actual (PositiveIntegerField, null)   # estudiantes
              + anio_egreso  (PositiveIntegerField, null)   # egresados/titulados
```
- Se piden en `completar_perfil` / preferencias (07). Mientras no existan, todo cae a
  "verifica" y el checklist es puramente informativo.

## UI
- En `convocatorias/detalle.html`: bloque "Requisitos" con íconos ✅/❌/⚠️ y leyenda
  "Esto es orientativo; tú decides si postular".
- Reusa estilo de chips/listas ya presentes; sin componentes nuevos pesados.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,2 | `checklist_requisitos` + detalle.html + test |
| CA-3 | rama de `postular` con messages no bloqueante + test |
| CA-4 | servicio aislado; `compatibilidad()` intacto |
| CA-5 | campos opcionales en PerfilTalento (tras sync gate) |
