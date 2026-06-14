# Modelo de Datos Canónico — specs

> Esquema único de entidades compartidas. Los `design.md` de cada feature **obedecen** este modelo.
> Detalle de campos de Convocatoria: [`../modelo-datos.md`](../modelo-datos.md) (raíz).

## Diagrama de entidades

```
Area (3) ──< Facultad (16) ──< Carrera (43)
                                   │
GrupoAfin >──M2M── Carrera ────────┘

Usuario (Django User + rol: egresado | admin | reclutador)
  ├─ Egresado    → carrera FK · estado_academico · 1──PerfilTalento
  ├─ Administrativo (rol vía AdminAllowlist)
  └─ Reclutador  → 1──Empresa

PerfilTalento
  ├─ preferencias (carreras_extra M2M · categorias_silenciadas · tipos_preferidos · frecuencia)
  ├─ credencial_publica (slug · activa · noindex)   # credencial verificable
  └─ Credencial (N) → tipo · detalle · fuente(verificado|autodeclarado) · visible_para_empresas

Empresa
  ├─ ruc · razon_social · nombre_comercial · tipo · ciiu
  ├─ telefono · direccion · web · linkedin · logo_url · banner_url · video_url · descripcion
  ├─ estado (pendiente | activa | rechazada)
  └─ es_referencial (derivado: sin reclutador vinculado)

Convocatoria
  ├─ empresa FK
  ├─ tipo (8) · titulo · descripcion · modalidad · ubicacion · duracion_estimada
  ├─ fecha_limite · medio_postulacion · email_contacto
  ├─ campos Nivel 2 (nullable, según tipo: subvencion/remuneracion, jornada, convenio, regimen…)
  ├─ campos Nivel 3 (nullable: banda_salarial, vacantes, beneficios, discapacidad…)
  ├─ carreras_objetivo M2M → Carrera
  ├─ estado (borrador|pendiente|publicada|observada|rechazada|caducada)
  ├─ transparencia_pct (calculado)
  └─ creada_por (empresa | admin)

Notificacion (in-app)  → usuario · tipo · leido
ResumenSemanal (log)   → usuario · convocatorias · enviado_en

# Config-as-data (tablas editables por admin)
ParametroLegal        → clave · valor   (RMV, topes jornada, plazos)
PesoTransparencia     → criterio · peso
ReglaElegibilidad     → estado_academico · tipo_convocatoria · permitido
AdminAllowlist        → email
```

## Reglas de integridad
- FKs hacia `Carrera` con `on_delete=PROTECT`; `Carrera.activa` para desactivar sin borrar.
- `Convocatoria.creada_por=admin` permite `Empresa.es_referencial`.
- Badge "Verificada" = `Empresa.estado==activa AND tiene reclutador`.
