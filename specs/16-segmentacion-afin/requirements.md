# Requisitos — 16 Segmentación por carreras afines

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../01-taxonomia/requirements.md`](../01-taxonomia/requirements.md), [`../05-matching/requirements.md`](../05-matching/requirements.md), [`../04-convocatorias/requirements.md`](../04-convocatorias/requirements.md).

## Objetivo
Hacer **operativa** la segmentación "X o afines" de [`../../propuesta.md`](../../propuesta.md) §8
(ej. "Administración o afines" → Administración, Economía, Contabilidad, Relaciones Industriales),
para que una empresa dirija una convocatoria a un **grupo de carreras relacionadas** sin
tener que marcarlas una por una, y que esos egresados la reciban.

## Contexto (estado actual del código)
- Existe el modelo `GrupoAfin` (`apps/taxonomia/models.py:64`) — "carreras o afines", editable por el admin. ✅
- Existe el seed `GRUPOS_AFINES` (`apps/taxonomia/management/commands/seed_taxonomia.py:97`). ✅
- Existe el helper `taxonomia/services.carreras_de(seleccion)` que expande Área/Facultad/**GrupoAfin** → carreras. ✅
- **PERO no está cableado:** el form de empresa (`ConvocatoriaForm`) solo expone `carreras_objetivo` (M2M a `Carrera`), y `matching.elegibles_por_carrera` (`apps/matching/services.py`) filtra por carrera individual. El `GrupoAfin` **no se usa en ninguna vista ni en el feed**. ❌

## Alcance
- **Incluye:** permitir seleccionar uno o más `GrupoAfin` al publicar/editar una convocatoria;
  al guardar, expandir el grupo a sus carreras miembro dentro de `carreras_objetivo`.
- **No incluye:** cambiar el algoritmo de ranking (Layer 3) ni el Gate 1; no se crea un campo
  de modelo nuevo (se reutiliza `carreras_objetivo`).

## Historias de usuario
- **HU-1:** Como empresa, quiero dirigir mi convocatoria a "Administración o afines" en un solo
  clic, en vez de marcar 4 carreras.
- **HU-2:** Como egresado de Economía, quiero ver una convocatoria dirigida a "Administración o
  afines" porque mi carrera pertenece a ese grupo.
- **HU-3:** Como admin, quiero editar qué carreras componen cada grupo afín sin tocar código.

## Criterios de aceptación (EARS)
- **CA-1:** Cuando una empresa publica una convocatoria y selecciona uno o más `GrupoAfin`, el
  sistema debe añadir **todas** las carreras miembro de esos grupos a `carreras_objetivo`.
- **CA-2:** Si una convocatoria quedó dirigida a un grupo afín, entonces un egresado cuya carrera
  pertenezca a ese grupo debe verla en su feed (Gate 2).
- **CA-3:** Cuando se combinan grupos afines y carreras sueltas, el sistema debe unir ambos
  conjuntos sin duplicar carreras.
- **CA-4:** Si el admin modifica las carreras de un `GrupoAfin`, entonces el cambio debe regir
  para las **nuevas** publicaciones (las ya expandidas conservan su selección — auditabilidad).

## Dependencias
- `01-taxonomia` (`GrupoAfin`, `carreras_de`), `04-convocatorias` (`ConvocatoriaForm`), `05-matching` (Gate 2).

## Notas legales / no funcionales aplicables
- Sin IA: la expansión es una unión de conjuntos sobre datos configurables (constitución §sin-IA).
- **Sync gate:** no se altera el modelo de datos congelado (se reutiliza `carreras_objetivo`); no requiere migración.
