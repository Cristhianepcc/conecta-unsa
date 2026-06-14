# Tareas — 05 Matching

## Implementación
- [x] T1 — App `matching` con `services.py` (sin modelos propios).
- [x] T2 — `elegibles_por_estado` leyendo `ReglaElegibilidad` (Gate 1).
- [x] T3 — `elegibles_por_carrera` (Gate 2, incluye carreras_extra de interés).
- [x] T4 — `rankear`/`puntuar` con reglas de afinidad + `motivo` explicable (Layer 3).
- [x] T5 — `feed(usuario)` que compone los 3 niveles (+ silenciar tipos).
- [x] T6 — `alcance(convocatoria)` para métricas.
- [x] Comando `seed_elegibilidad` (matriz config-as-data 3×8 = 24 reglas).

## Pruebas
- [x] T7 — test CA-1: estudiante no ve "empleo"; egresado no ve "preprofesional".
- [x] T8 — test CA-2: solo convocatorias de su carrera/afines.
- [x] T9 — test CA-3/4: orden por afinidad + motivo correcto (verificada pesa más).
- [x] T10 — test CA-5: feed funciona sin perfil completo.
- [x] CA-6 (alcance), CA-7 (matriz desde BD).

## Cierre
- [x] DoD cumplido — 10 tests EARS verdes.

> Notas:
> - Sin IA: Gate 1/2 = querysets encadenados; Layer 3 = puntaje explicable (motivo legible).
> - Matriz de elegibilidad en `ReglaElegibilidad` (CA-7): agregar estado/tipo = filas nuevas.
> - Reglas de afinidad credencial→tipo en `RELEVANCIA_CREDENCIAL`; verificada pesa 15 vs 10.
