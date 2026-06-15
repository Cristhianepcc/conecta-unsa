# Requisitos — 18 Plantillas reutilizables de convocatoria

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../04-convocatorias/requirements.md`](../04-convocatorias/requirements.md), [`../11-dashboard-empresa/requirements.md`](../11-dashboard-empresa/requirements.md).

## Objetivo
Cumplir [`../../propuesta.md`](../../propuesta.md) §6.2 ("plantillas reutilizables") y §6.3
("mínima fricción"): reducir el esfuerzo de publicar ofreciendo **plantillas pre-llenadas por tipo**
de convocatoria (práctica, empleo, voluntariado…) que la empresa puede ajustar antes de publicar.

## Contexto (estado actual del código)
- El sidebar de empresa muestra "Guía y plantillas" pero **solo enlaza a la guía**
  (`core:como_funciona`); no existen plantillas reales (`apps/empresas/templates/empresas/_sidebar_empresa.html:7`). ❌
- El formulario de 3 niveles (`ConvocatoriaForm` + `_form.html`) ya guía la mejora progresiva. ✅

## Alcance
- **Incluye:** modelo `PlantillaConvocatoria` (config-as-data, editable por admin), selector de
  plantilla al iniciar una publicación, y pre-llenado del `ConvocatoriaForm` con sus valores.
- **No incluye:** plantillas privadas por empresa (v1 son institucionales/compartidas), versionado.

## Historias de usuario
- **HU-1:** Como empresa, quiero partir de una plantilla "Práctica preprofesional" con los campos
  típicos ya llenos y solo ajustar lo mío.
- **HU-2:** Como admin, quiero crear/editar plantillas sin tocar código para estandarizar la calidad.
- **HU-3:** Como universidad, quiero que las publicaciones tengan mejor estructura desde el inicio.

## Criterios de aceptación (EARS)
- **CA-1:** El admin debe poder crear una `PlantillaConvocatoria` con tipo y valores por defecto
  (título sugerido, descripción, modalidad, niveles 2/3 aplicables).
- **CA-2:** Cuando una empresa elige una plantilla al publicar, el formulario debe aparecer
  **pre-llenado** con los valores de la plantilla.
- **CA-3:** Si la empresa modifica un campo pre-llenado, entonces se debe guardar el valor editado
  (la plantilla es punto de partida, no obligación).
- **CA-4:** Mientras no exista ninguna plantilla, la publicación debe seguir funcionando con el
  formulario en blanco (degradación elegante).

## Dependencias
- `04-convocatorias` (`ConvocatoriaForm`), `11-dashboard-empresa` (publicar), Django admin (alta de plantillas).

## Notas legales / no funcionales aplicables
- **Sync gate:** introduce el modelo `PlantillaConvocatoria` → proponer en
  [`../modelo-datos.md`](../modelo-datos.md) antes de implementar (modelo congelado).
- Config-as-data: las plantillas son contenido editable, no código.
