# Tareas — 15 Empleabilidad

## Implementación
- [ ] T1 (sync gate) — Proponer `Evento` en `modelo-datos.md`; crear app `empleabilidad`,
  modelo + migración (incluir app en `INSTALLED_APPS` y `urls.py` raíz si `00` no lo dejó).
- [ ] T2 — `services.eventos_para(usuario)` (futuros + carrera del perfil / abiertos).
- [ ] T3 — `services.publicar_evento(evento)` → `notificar` in-app segmentado por carrera.
- [ ] T4 — Alta de eventos en Django admin (MVP) con `carreras_objetivo`.
- [ ] T5 — Sección/ruta de empleabilidad para el egresado + tarjeta de evento (enlace
  externo de inscripción).

## Pruebas
- [ ] T6 — test CA-2: egresado de carrera X ve evento dirigido a X; no ve el dirigido solo a Y.
- [ ] T7 — test CA-3: `publicar_evento` notifica solo a egresados de las carreras objetivo.
- [ ] T8 — test CA-4: evento pasado no aparece en `eventos_para`.

## Cierre
- [ ] DoD — tests EARS verdes + evento de demo en `seed_demo`.

> Nota: cubre el insight 4 (acompañamiento) reusando la campana/comunicados existentes.
> Inscripción externa: la plataforma difunde y orienta, no gestiona el evento.
