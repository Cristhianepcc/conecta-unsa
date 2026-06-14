# Diseño — 06 Flujo Admin

## App
`convocatorias` (servicios de flujo) + `core` (parámetros).

## Servicios
```
calcular_alertas(conv) → set[Alerta]          # duplicado, incompleta, baja_transparencia, exceso
detectar_duplicado(conv) → [(otra, similitud)]  # pg_trgm: misma empresa + título similar + ≤30d
decidir_publicacion(conv) → 'auto' | 'revision'  # semáforo de confianza
observar(conv, comentario) · aprobar(conv) · rechazar(conv)
caducar_vencidas()                            # comando para cron
```

## Detección de duplicados (pg_trgm)
- `similarity(normalizar(titulo_a), normalizar(titulo_b)) > umbral` (umbral en ParametroLegal),
  filtrando misma empresa y `fecha <= 30d`. El admin **confirma** (no se borra solo).

## Estados y transiciones
- borrador → pendiente → {publicada | observada | rechazada}; cualquiera vigente → caducada.
- "Activa" = property derivada (publicada y `hoy <= fecha_limite`). "Archivada" = caducada/archivada.

## Configuración
- Umbral de similitud y límite de "exceso de difusión" en `ParametroLegal` (config-as-data).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1 | máquina de estados + test |
| CA-2 | `calcular_alertas` + test |
| CA-3 | `detectar_duplicado` (pg_trgm) + test |
| CA-4,5 | `decidir_publicacion` + test |
| CA-6 | `observar` + notificación (08) |
| CA-7 | `caducar_vencidas` (cron) + test |
