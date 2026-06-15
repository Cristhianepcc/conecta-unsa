# Tareas — 14 Requisitos de postulación

## Implementación
- [ ] T1 — Servicio `apps/convocatorias/requisitos.py:checklist_requisitos(conv, perfil)`
  (evalúa `ciclo_minimo`, `tiempo_egreso_meses`; estados cumple/no_cumple/verifica).
- [ ] T2 — Mostrar el checklist en `convocatorias/detalle.html` (íconos + leyenda
  "orientativo, no bloqueante").
- [ ] T3 — En `convocatorias/views.py:postular`, aviso no bloqueante si hay `no_cumple`
  (Django messages) y continuar con el redirect.
- [ ] T4 (sync gate) — Proponer y, si se aprueba, añadir `ciclo_actual` y `anio_egreso` a
  `PerfilTalento` (+ migración) y capturarlos en `07`.

## Pruebas
- [ ] T5 — test CA-1/CA-2 con perfil completo: requisito que se cumple → ✅; que no → ❌.
- [ ] T6 — test CA-2 con perfil sin dato → ⚠️ "verifica".
- [ ] T7 — test CA-3: `postular` con `no_cumple` deja mensaje y **sí** redirige (no bloquea).
- [ ] T8 — test CA-4: `compatibilidad()` no cambia su salida.

## Cierre
- [ ] DoD — tests EARS verdes. (T4/CA-5 quedan tras sync gate del modelo-datos.)

> Nota: aprovecha campos ya capturados (`ciclo_minimo`, `tiempo_egreso_meses`) sin duplicar
> datos. Ataca el insight 5 ("postulantes alineados") **informando**, sin que la plataforma
> seleccione ni reciba candidatos.
