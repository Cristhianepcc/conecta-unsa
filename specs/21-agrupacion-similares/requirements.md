# Requisitos — 21 Agrupación de convocatorias similares

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../06-flujo-admin/requirements.md`](../06-flujo-admin/requirements.md), [`../08-notificaciones/requirements.md`](../08-notificaciones/requirements.md).

## Objetivo
Cubrir [`../../propuesta.md`](../../propuesta.md) §6.2 ("agrupación de convocatorias similares") y
§9 ("saturación temática → consolidar publicaciones similares en resúmenes"): agrupar convocatorias
**parecidas pero no idénticas** (mismo tipo + carreras + ventana temporal) para reducir saturación
en el digest del egresado y dar contexto al admin.

## Contexto (estado actual del código)
- Existe detección de **duplicados exactos** por empresa + título similar (`flujo.detectar_duplicado`). ✅
- El digest semanal ya **consolida en un solo correo** por egresado (`notificaciones/services.enviar_resumen_a`). ✅
- **PERO no agrupa similares no idénticos** (p. ej. tres "prácticas de marketing" de empresas
  distintas) ni en el digest ni en la bandeja admin. ❌

## Alcance
- **Incluye:** servicio que agrupa un conjunto de convocatorias por similitud temática
  (tipo + carreras objetivo + ventana), su uso en el digest (mostrar "y N similares") y una vista
  agrupada opcional en la bandeja admin.
- **No incluye:** fusión/borrado de convocatorias (no se elimina nada — auditabilidad), clustering
  con IA/embeddings (reglas transparentes únicamente).

## Historias de usuario
- **HU-1:** Como egresado, quiero que el resumen consolide convocatorias parecidas en vez de
  listarlas todas sueltas.
- **HU-2:** Como admin, quiero ver convocatorias similares agrupadas para revisarlas juntas.

## Criterios de aceptación (EARS)
- **CA-1:** Dado un conjunto de convocatorias, el sistema debe agruparlas cuando compartan **tipo**
  y **al menos una carrera objetivo** dentro de una ventana temporal configurable.
- **CA-2:** Cuando el digest contiene un grupo de similares, debe mostrar un representante y la
  cuenta "y N más similares" en lugar de N entradas separadas.
- **CA-3:** Si una convocatoria no tiene similares, entonces se debe mostrar individualmente (sin grupo).
- **CA-4:** La agrupación **no** debe ocultar ni borrar convocatorias: todas siguen accesibles desde
  el feed/detalle.

## Dependencias
- `06-flujo-admin` (bandeja), `08-notificaciones` (digest), `04-convocatorias` (modelo), `01-taxonomia` (carreras).

## Notas legales / no funcionales aplicables
- Sin IA: agrupación por reglas (tipo + carrera + ventana), auditable.
- **Sync gate:** sin modelo nuevo (agrupación calculada en memoria); ventana en `ParametroLegal`.
