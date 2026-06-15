# Requisitos — 19 Monitoreo de volumen por empresa (control de exceso de difusión)

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../06-flujo-admin/requirements.md`](../06-flujo-admin/requirements.md), [`../03-empresas/requirements.md`](../03-empresas/requirements.md).

## Objetivo
Cubrir [`../../propuesta.md`](../../propuesta.md) §6.4, §7-Paso 2 ("posibles excesos de difusión")
y §9 ("empresas con publicaciones excesivas → límites de frecuencia y monitoreo"): detectar y
**alertar** (no bloquear) cuando una empresa publica por encima de un umbral en una ventana de tiempo.

## Contexto (estado actual del código)
- Existe detección de **duplicados** por empresa (`flujo.detectar_duplicado`, pg_trgm). ✅
- Existe la **bandeja admin con riesgo** alto/medio/ok y `calcular_alertas` (`apps/core/views.py`, `apps/convocatorias/flujo.py`). ✅
- **PERO no hay control de volumen/frecuencia por empresa:** nada cuenta cuántas convocatorias
  publicó una empresa en N días ni alerta por exceso. ❌

## Alcance
- **Incluye:** servicio que cuenta publicaciones recientes por empresa, alerta de "exceso de
  difusión" en la bandeja admin cuando supera un umbral configurable, y visibilidad del dato.
- **No incluye:** bloqueo automático de publicación, sanciones, cuotas duras (la propuesta pide
  **monitoreo**, no censura).

## Historias de usuario
- **HU-1:** Como admin, quiero ver si una empresa está publicando en exceso para revisarla.
- **HU-2:** Como universidad, quiero controlar la saturación del canal sin frenar la actividad legítima.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe contar las convocatorias de una empresa publicadas/creadas dentro de
  una ventana configurable (p. ej. 7 días).
- **CA-2:** Si una empresa supera el umbral configurable de publicaciones en la ventana, entonces
  el sistema debe marcar una **alerta de "exceso de difusión"** en su convocatoria/bandeja admin.
- **CA-3:** Mientras la empresa esté por debajo del umbral, el sistema **no** debe alterar el flujo
  (sin alerta, sin bloqueo).
- **CA-4:** El umbral y la ventana deben ser **configurables** por el admin (config-as-data).

## Dependencias
- `06-flujo-admin` (`calcular_alertas`, bandeja), `03-empresas` (`Empresa`), `00-fundacion` (`ParametroLegal`).

## Notas legales / no funcionales aplicables
- **No bloquea:** solo monitorea (proporcionalidad; coherente con la propuesta).
- **Sync gate:** sin modelo nuevo (cuenta sobre `Convocatoria`); umbral/ventana en `ParametroLegal`.
