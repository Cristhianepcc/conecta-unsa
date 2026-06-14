# Diseño — 07 Perfil y Credencial

## App
`usuarios`

## Modelos
```
PerfilTalento
  ├─ egresado : OneToOne → Usuario
  ├─ # preferencias
  │   carreras_extra : M2M → Carrera
  │   categorias_silenciadas · tipos_preferidos · frecuencia (default semanal)
  └─ # credencial pública
      cred_activa : Bool(default False) · cred_slug : Slug(unique)

Credencial
  ├─ perfil : FK → PerfilTalento
  ├─ tipo : enum(idioma, taller, beca, olimpiada, voluntariado, intercambio,
  │           representacion, evento, incubadora_jaku, practica_convalidada, articulo, tesis)
  ├─ detalle : JSON/Char (nombre, nivel, fecha)
  ├─ fuente : enum(verificado, autodeclarado)
  └─ visible_para_empresas : Bool(default False)
```

## Vistas / rutas
| Ruta | Rol | Descripción |
|---|---|---|
| `/completar-perfil` | egresado | carrera + estado (primer ingreso) |
| `/perfil` | egresado | editar credenciales autodeclaradas + preferencias |
| `/perfil/credencial` | egresado | activar/revocar URL + visibilidad |
| `/credencial/<slug>` | público | carta de presentación (solo lectura, noindex) |

## Decisiones
- Verificado = solo lectura (badge 🟢); autodeclarado = editable. En demo todo es autodeclarado.
- Credencial pública: **no social** (sin feed/conexiones), solo por link, `noindex`, revocable.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | `/completar-perfil` + test |
| CA-2,3 | Credencial.fuente + permisos edición + test |
| CA-4 | preferencias + test |
| CA-5,6,7 | credencial pública (slug, noindex, revocar) + test |
