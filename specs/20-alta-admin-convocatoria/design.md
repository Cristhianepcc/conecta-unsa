# Diseño — 20 Alta de convocatoria por el administrativo

> Coherente con [`../modelo-datos.md`](../modelo-datos.md) y [`../constitucion.md`](../constitucion.md).

## App / módulo Django
`core` (panel admin) reusando `convocatorias` (form/flujo). Sin modelo nuevo.

## Modelos
Sin cambios. Se usa:
```
Convocatoria.creada_por = CREADA_POR_ADMIN      # ya existe
Convocatoria.empresa    → seleccionada por el admin
```

## Servicios (lógica de negocio)
- Reusa `ConvocatoriaForm` con un campo extra **visible solo para admin**: `empresa`
  (`ModelChoiceField(Empresa.objects.filter(estado=activa))`).
- Reusa `flujo` (faltantes de nivel 1 + `detectar_duplicado`) — sin lógica nueva de validación.

## Vistas / rutas
| Ruta | Método | Rol | Descripción |
|---|---|---|---|
| `/panel-admin/convocatoria/nueva/` | GET/POST | admin | alta manual; setea `empresa` y `creada_por=admin` |

- Decorador `admin_required` (CA-4).
- Al guardar: `obj.creada_por = CREADA_POR_ADMIN`; estado inicial según flujo (borrador/pendiente),
  luego el admin la revisa/publica con el flujo existente.

## Templates / UI
- Reusa `_form.html` + selector de empresa al inicio.
- Entrada desde el panel admin: botón "Registrar convocatoria recibida".
- Ayuda: "Pega aquí el contenido recibido por correo; quedará a nombre de la empresa elegida."

## Configuración (config-as-data)
- Ninguna nueva.

## Decisiones de diseño
- **Reúso total** de form + flujo → la convocatoria admin es indistinguible aguas abajo, salvo por
  `creada_por` (trazabilidad, CA-2).
- Ingesta automática de correo (IMAP/parser) se deja fuera: el copiado manual cubre el caso real
  del MVP sin dependencias frágiles.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | vista alta + `ConvocatoriaForm` + selector empresa + test |
| CA-2 | `creada_por=admin` al guardar + test |
| CA-3 | reúso de `flujo` (faltantes + duplicados) + test |
| CA-4 | `admin_required` + test 403 |
