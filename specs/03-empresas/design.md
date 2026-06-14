# Diseño — 03 Empresas

## App
`empresas`

## Modelos
```
Empresa
  ├─ ruc : Char(unique)
  ├─ razon_social · nombre_comercial · tipo · ciiu
  ├─ telefono · direccion · web · linkedin
  ├─ logo_url · banner_url · video_url · descripcion
  └─ estado : enum(pendiente, activa, rechazada)

Reclutador
  ├─ usuario : OneToOne → Usuario(rol=reclutador)
  ├─ empresa : OneToOne → Empresa     # 1 por empresa (MVP)
  └─ dni · nombres · ap_paterno · ap_materno · cargo · email · telefono
```
- `Empresa.es_referencial` = property: `not hasattr(self, 'reclutador')`.
- `Empresa.verificada` = property: `estado==activa and not es_referencial`.

## Vistas / rutas
| Ruta | Rol | Descripción |
|---|---|---|
| `/empresa/registro` | público | RUC → form (bloque A + B) |
| Django Admin | admin | activar/rechazar; crear empresa referencial |

## UI
- Registro estilo UNI (`login-empresa-imagenes/`): paso RUC → formulario 2 bloques.
- Mensaje "tu cuenta será verificada por la universidad".

## Configuración
- Activación = acción del admin en Django Admin (panel híbrido).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,7 | vista registro + unique RUC + test |
| CA-2 | guard `empresa.verificada` antes de publicar + test |
| CA-3 | acción admin + property verificada + test |
| CA-4 | empresa referencial (sin reclutador) + test |
| CA-6 | campos URL |
