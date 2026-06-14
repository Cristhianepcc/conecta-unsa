# Diseño — 01 Taxonomía

> Cómo. Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
`taxonomia` — datos de referencia académicos. Sin lógica de negocio pesada; solo estructura + expansión.

## Modelos
```
Area
  ├─ nombre : Char(unique)
  └─ orden : Int

Facultad
  ├─ nombre : Char(unique)
  └─ area : FK → Area

Carrera
  ├─ nombre : Char(unique)
  ├─ facultad : FK → Facultad
  └─ activa : Bool (default True)

GrupoAfin
  ├─ nombre : Char(unique)            # ej. "Administración o afines"
  ├─ carreras : M2M → Carrera
  └─ editable_por_admin : (siempre; config-as-data)
```

## Servicios (lógica de negocio)
- `expandir(seleccion)` → recibe Áreas / Facultades / Carreras / GrupoAfines y devuelve un
  **set único de Carreras**. Regla explícita: Área → todas sus Facultades → sus Carreras activas;
  Facultad → sus Carreras activas; GrupoAfin → sus carreras. (Soporta CA-4.)

## Vistas / rutas
- Sin vistas públicas propias. La gestión se hace vía **Django Admin** (panel híbrido) → CA-2/CA-3 gratis.

## Templates / UI
- N/A propia. Se consume desde selects/targeting en `convocatorias` y filtros del egresado.

## Configuración (config-as-data)
- **Toda** la taxonomía y los GrupoAfin son editables desde Django Admin. Es el ejemplo canónico
  del principio "configuración-como-datos" de la constitución.

## Decisiones de diseño
- **Carrera = unidad atómica** (matching Gate 2): el targeting siempre se resuelve a carreras
  → por eso `expandir()` colapsa cualquier nivel a un set de Carreras.
- **`activa` en Carrera** (no borrar): permite "desactivar" sin romper integridad (apoya CA-5).
- **`on_delete=PROTECT`** en FKs hacia Carrera desde convocatorias/egresados (apoya CA-5).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | Modelos + seed (`seed-demo.md`) + test conteo |
| CA-2, CA-3 | Django Admin sobre los modelos + test |
| CA-4 | Servicio `expandir()` + test |
| CA-5 | `PROTECT` / `activa` + test de borrado |
| CA-6 | Comando/fixture de seed + test |
