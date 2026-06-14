# Diseño — 05 Matching

## App
`matching` (solo servicios, sin modelos propios).

## Servicios
```
elegibles_por_estado(usuario, qs) → qs        # Gate 1: filtra por ReglaElegibilidad(estado×tipo)
elegibles_por_carrera(usuario, qs) → qs       # Gate 2: carrera ∈ carreras_objetivo
rankear(usuario, qs) → [(conv, puntaje, motivo)]  # Layer 3: puntaje + explicación
feed(usuario) → lista ordenada                # compone los 3
alcance(convocatoria) → int                   # conteo de egresados que califican
```

### Reglas de ranking (explicables, sin IA)
- +peso por cada credencial del perfil que coincide con un requisito/atributo de la convocatoria
  (idioma↔requiere idioma, tesis/artículo↔investigación, liderazgo↔trainee, etc.).
- +peso si modalidad/ubicación preferida coincide.
- `motivo` = lista legible de las coincidencias que sumaron.

## Decisiones
- Gate 1 y 2 son **filtros duros** (querysets encadenados → eficiente).
- Layer 3 **no oculta**, solo ordena.
- Toda la elegibilidad sale de `ReglaElegibilidad` (CA-7) → agregar posgrado = filas nuevas.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,7 | `elegibles_por_estado` + ReglaElegibilidad + test |
| CA-2 | `elegibles_por_carrera` + test |
| CA-3,4 | `rankear` (puntaje + motivo) + test |
| CA-5 | `feed` sin perfil → solo filtros |
| CA-6 | `alcance` + test |
