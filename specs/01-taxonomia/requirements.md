# Requisitos — 01 Taxonomía

> Qué y por qué. Obedece [`../constitucion.md`](../constitucion.md).
> Referencia: [`../../taxonomia-unsa.md`](../../taxonomia-unsa.md), [`../../matching.md`](../../matching.md).

## Objetivo
Modelar la estructura académica de la UNSA (Área → Facultad → Carrera) y los grupos "o afines"
como **datos editables por el admin**, para que toda la segmentación del sistema se construya
sobre ella sin tocar código.

## Alcance
- **Incluye:** entidades Área, Facultad, Carrera, GrupoAfin; CRUD por admin; seed inicial; expansión multinivel.
- **No incluye:** la lógica de matching en sí (vive en `05-matching`); UI pública (vive en las pantallas).

## Historias de usuario
- **HU-1:** Como administrativo, quiero gestionar áreas, facultades y carreras sin programar,
  para mantener la taxonomía actualizada.
- **HU-2:** Como administrativo, quiero crear grupos "o afines" (conjuntos nombrados de carreras),
  para dirigir convocatorias a carreras relacionadas.
- **HU-3:** Como sistema, quiero expandir una selección de Área o Facultad a sus carreras,
  para que el targeting siempre se resuelva a carreras concretas.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe almacenar la jerarquía **3 Áreas → 16 Facultades → 43 Carreras**
  según [`../../taxonomia-unsa.md`](../../taxonomia-unsa.md).
- **CA-2:** Cuando el admin crea/edita/elimina un Área, Facultad o Carrera desde el panel,
  el sistema debe persistir el cambio **sin requerir despliegue de código**.
- **CA-3:** Cuando el admin crea un GrupoAfin con un nombre y un conjunto de carreras,
  el sistema debe guardarlo y dejarlo disponible para targeting.
- **CA-4:** Cuando se solicita expandir un Área o una Facultad, el sistema debe devolver
  el conjunto **finito y explícito** de carreras que contiene (nunca "todas").
- **CA-5:** Si se intenta eliminar una Carrera referenciada por convocatorias o egresados,
  entonces el sistema debe impedirlo (o exigir reasignación) para no romper integridad.
- **CA-6:** Al inicializar, el sistema debe sembrar la taxonomía completa y un set base de
  GrupoAfin (ej. "Administración o afines", "Ingenierías o afines", "Salud o afines").

## Dependencias
- Spec previa: `00-fundacion` (proyecto Django + Postgres listos).
- Docs: `taxonomia-unsa.md`, `matching.md` (Gate 2 y GrupoAfin).

## Notas legales / no funcionales
- N/A legal directo. NFR: la edición es solo para rol **admin** (ver `../requisitos-no-funcionales.md`).
