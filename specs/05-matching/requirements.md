# Requisitos — 05 Matching

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../matching.md`](../../matching.md).

## Objetivo
Decidir **qué convocatorias ve cada usuario y en qué orden** mediante 3 niveles de reglas
transparentes (sin IA): elegibilidad legal, carrera y ranking por perfil.

## Alcance
- **Incluye:** Gate 1 (estado×tipo), Gate 2 (carrera), Layer 3 (ranking explicable), motivo de recomendación.
- **No incluye:** el perfil/credenciales en sí (`07`), la UI del feed (`10`).

## Historias de usuario
- **HU-1:** Como egresado, quiero ver solo convocatorias para las que califico (por ley y carrera).
- **HU-2:** Como egresado, quiero que lo más afín a mi perfil aparezca primero y saber por qué.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe excluir convocatorias cuyo **tipo no es elegible** para el estado académico del usuario (según `ReglaElegibilidad`).
- **CA-2:** El sistema debe excluir convocatorias cuyas **carreras objetivo** no incluyen la carrera del usuario.
- **CA-3:** El sistema debe **ordenar** las convocatorias elegibles por un puntaje de afinidad calculado de las credenciales del perfil.
- **CA-4:** Cuando una convocatoria aparece recomendada, el sistema debe poder **explicar el motivo** ("coincide con X, Y").
- **CA-5:** Mientras el usuario no tenga perfil completo, el sistema debe igual mostrar el feed (filtros funcionan sin ranking).
- **CA-6:** El sistema debe resolver el alcance de una convocatoria como el **conteo de egresados** cuyas carreras/estado califican (para métricas).
- **CA-7:** El sistema debe leer la matriz de elegibilidad desde `ReglaElegibilidad` (config-as-data), no hardcodeada.

## Dependencias
- `01-taxonomia`, `04-convocatorias`, `07-perfil` (credenciales), `00` (ReglaElegibilidad).

## Notas
- Sin IA: filtros = querysets; ranking = función de puntaje explicable.
