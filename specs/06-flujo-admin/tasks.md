# Tareas — 06 Flujo Admin

## Implementación
- [x] T1 — Máquina de estados de Convocatoria (transiciones válidas) + property `activa`.
- [x] T2 — `calcular_alertas` (duplicado, incompleta, baja transparencia, exceso).
- [x] T3 — `detectar_duplicado` con pg_trgm (umbral en ParametroLegal).
- [x] T4 — `decidir_publicacion` (semáforo: verificada + sin alertas + 🟢 → auto) + `procesar_envio`.
- [x] T5 — `observar/aprobar/rechazar` + registro de comentario (hook de notificación para 08).
- [x] T6 — Comando `caducar_vencidas` (para cron).

## Pruebas
- [x] T7 — test CA-3: títulos similares de misma empresa → alerta duplicado (pg_trgm).
- [x] T8 — test CA-4: verificada + 🟢 + sin alertas → auto-publica.
- [x] T9 — test CA-5: empresa referencial / con alertas → pendiente.
- [x] T10 — test CA-7: vencida → caducada.
- [x] CA-1 (transiciones), CA-2 (alertas), CA-6 (observar registra comentario).

## Cierre
- [x] DoD cumplido — 13 tests EARS verdes.

> Notas:
> - Duplicados con pg_trgm (TrigramSimilarity sobre título en minúsculas); umbral y límite de
>   difusión son config-as-data (ParametroLegal). El admin confirma; el sistema no borra solo.
> - `observar()` llama un hook de notificación que la feature 08 implementará (CA-6 completo).
