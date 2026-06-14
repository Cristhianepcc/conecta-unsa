# Tareas — 06 Flujo Admin

## Implementación
- [ ] T1 — Máquina de estados de Convocatoria (transiciones válidas) + property "activa".
- [ ] T2 — `calcular_alertas` (duplicado, incompleta, baja transparencia, exceso).
- [ ] T3 — `detectar_duplicado` con pg_trgm (umbral en ParametroLegal).
- [ ] T4 — `decidir_publicacion` (semáforo: verificada + sin alertas + 🟢 → auto).
- [ ] T5 — `observar/aprobar/rechazar` + registro de comentario.
- [ ] T6 — Comando `caducar_vencidas` (para cron).

## Pruebas
- [ ] T7 — test CA-3: títulos similares de misma empresa → alerta duplicado.
- [ ] T8 — test CA-4: verificada + 🟢 + sin alertas → auto-publica.
- [ ] T9 — test CA-5: empresa nueva o con alertas → pendiente.
- [ ] T10 — test CA-7: vencida → caducada.

## Cierre
- [ ] DoD cumplido.
