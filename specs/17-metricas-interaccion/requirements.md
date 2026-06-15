# Requisitos — 17 Métricas de interacción y alcance (panel admin)

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../12-panel-admin/requirements.md`](../12-panel-admin/requirements.md), [`../10-dashboard-estudiante/requirements.md`](../10-dashboard-estudiante/requirements.md).

## Objetivo
Exponer en el panel admin los **indicadores de éxito** de [`../../propuesta.md`](../../propuesta.md) §12
que hoy se registran pero no se muestran: interacción con convocatorias y alcance pertinente.
Permite a la institución medir si el canal recuperó utilidad (insight central de la propuesta).

## Contexto (estado actual del código)
- Se registran interacciones: `InteraccionConvocatoria` (tipo `vista`/`guardada`) en
  `apps/convocatorias/models.py:193`, vía `interacciones.registrar_vista` / `alternar_guardada`. ✅
- El panel admin (`apps/core/views.py:113`) ya muestra `recibidas / pendientes / validadas` y
  conteo de `duplicados`. ✅
- **PERO no expone interacción ni alcance:** no hay vistas totales, guardadas, ni top de
  convocatorias por interacción, ni nº de egresados elegibles ("alcance pertinente"). ❌

## Alcance
- **Incluye:** bloque de métricas de interacción en el panel admin (vistas, guardadas, % de
  convocatorias con al menos una interacción, top N por interacción) y una métrica de alcance
  pertinente por convocatoria (nº de egresados elegibles vía Gate 1+2).
- **No incluye:** dashboards de series temporales/gráficos avanzados, export CSV (futuro),
  métricas por empresa (cubierto parcialmente en 19).

## Historias de usuario
- **HU-1:** Como admin, quiero ver cuántas vistas y guardados generaron las convocatorias para
  saber si el canal es útil.
- **HU-2:** Como admin, quiero ver las convocatorias con más interacción para replicar buenas prácticas.
- **HU-3:** Como universidad, quiero una métrica de "alcance pertinente" (a cuántos egresados
  elegibles llegó), no de difusión masiva.

## Criterios de aceptación (EARS)
- **CA-1:** El panel admin debe mostrar el total de **vistas** y de **guardados** de convocatorias.
- **CA-2:** El panel admin debe mostrar el **top N** de convocatorias por número de interacciones.
- **CA-3:** Para una convocatoria publicada, el sistema debe poder calcular su **alcance pertinente**
  = nº de egresados que pasan Gate 1 (estado) + Gate 2 (carrera).
- **CA-4:** Si no hay interacciones registradas, entonces el panel debe mostrar ceros sin error
  (estado vacío correcto).

## Dependencias
- `10-dashboard-estudiante` (`InteraccionConvocatoria`), `05-matching` (Gates), `12-panel-admin` (panel).

## Notas legales / no funcionales aplicables
- Métricas **agregadas** (no exponer datos personales de egresados) — privacidad (`../requisitos-no-funcionales.md`).
- Sin IA: agregaciones SQL simples (`count`, `annotate`).
