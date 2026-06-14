# Diseño — <NOMBRE DE LA FEATURE>

> Cómo. Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
<Nombre de la app y su responsabilidad.>

## Modelos
```
<Entidad>
  ├─ campo : tipo  (restricciones)
  └─ relación → <Otra entidad>
```

## Servicios (lógica de negocio)
- `<servicio>(...)` → <qué hace, qué devuelve; reglas explícitas, sin IA>.

## Vistas / rutas
| Ruta | Método | Rol | Descripción |
|---|---|---|---|
| `/...` | GET/POST | <rol> | <…> |

## Templates / UI
- <pantallas, componentes, estados (vacío, error, carga)>.

## Configuración (config-as-data)
- <qué parámetros van en tabla editable por el admin>.

## Decisiones de diseño
- <decisión → por qué>.

## Trazabilidad
| Criterio (requirements) | Cubierto por |
|---|---|
| CA-1 | <modelo/servicio/vista + test> |
