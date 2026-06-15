# Requisitos — 14 Requisitos de postulación (cumples / no cumples)

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../05-matching/requirements.md`](../05-matching/requirements.md), [`../07-perfil-credencial/requirements.md`](../07-perfil-credencial/requirements.md).

## Objetivo
Reducir **postulaciones irrelevantes** mostrando al egresado, antes de postular, un
checklist transparente de los requisitos de la convocatoria que **ya se capturan** pero hoy
no se usan en el lado del candidato (`ciclo_minimo`, `tiempo_egreso_meses`). El egresado que
no califica se auto-descarta — sin que la plataforma seleccione (coherente con `propuesta.md`).

## Contexto (estado actual del código)
- `ciclo_minimo` y `tiempo_egreso_meses` existen en `Convocatoria` (`models.py:80-81`), se
  piden en el form y se muestran al empleador, pero **no se usan en el matching ni del lado
  del egresado**.
- `PerfilTalento` tiene `estado_academico` y `carrera`, pero **no** guarda `ciclo_actual`
  ni año/fecha de egreso → hoy no hay dato para auto-evaluar esos requisitos.

## Alcance
- **Incluye:** mostrar un checklist de requisitos en el detalle y antes de postular.
  Auto-evaluar lo evaluable con los datos del perfil; lo no evaluable se muestra como
  "verifica que cumples".
- **No incluye:** bloquear la postulación (la plataforma **no** selecciona — solo informa),
  ni recibir/gestionar candidatos.

## Historias de usuario
- **HU-1:** Como egresado, antes de postular quiero ver claramente qué pide la convocatoria
  (ciclo mínimo, tiempo máximo de egreso) para no perder tiempo si no califico.
- **HU-2:** Como empresa, quiero recibir menos postulaciones de perfiles que no cumplen los
  requisitos básicos.

## Criterios de aceptación (EARS)
- **CA-1:** En el detalle de una convocatoria, el sistema debe mostrar un **checklist de
  requisitos** con `ciclo_minimo` y `tiempo_egreso_meses` cuando estén definidos.
- **CA-2:** Cuando el perfil tiene el dato necesario, el sistema debe marcar cada requisito
  como **cumple ✅ / no cumple ❌**; cuando no lo tiene, como **"verifica" ⚠️** (neutral).
- **CA-3:** Antes de redirigir al medio de postulación, si el egresado **no cumple** algún
  requisito evaluable, el sistema debe mostrar un **aviso no bloqueante** ("revisa que
  cumples los requisitos") y permitir continuar igual.
- **CA-4:** El checklist **no debe** exponer datos de otros usuarios ni alterar el % de
  compatibilidad existente (`compatibilidad()` no se toca).
- **CA-5 (opcional, sync gate):** Si se añaden `ciclo_actual` y `anio_egreso` a
  `PerfilTalento`, el sistema debe usarlos para evaluar CA-2 automáticamente.

## Dependencias
- `04-convocatorias` (campos y detalle/postular), `07-perfil` (datos del talento),
  `05-matching` (no se modifica; solo se lee el perfil).

## Notas
- **Sync gate (modelo-datos):** CA-5 requiere proponer `ciclo_actual` y `anio_egreso` en
  `PerfilTalento`. Mientras no se acuerde, el checklist funciona en modo informativo (CA-2
  cae a "verifica").
- Principio rector: **informar, no seleccionar** — la línea que `propuesta.md §3/§7` prohíbe
  cruzar.
