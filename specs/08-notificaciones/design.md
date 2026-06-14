# Diseño — 08 Notificaciones

## App
`notificaciones`

## Modelos
```
Notificacion        → usuario · tipo · mensaje · url · leido(bool) · creado
ResumenSemanalLog   → usuario · convocatorias(M2M) · enviado_en
```

## Servicios / comandos
```
construir_resumen(egresado) → contexto (usa matching.feed + filtra silenciadas)
enviar_resumenes()  → comando manage.py (cron semanal): por egresado con novedades, manda 1 correo
notificar(usuario, tipo, mensaje, url)  → crea Notificacion in-app
```

## Correo (Resend)
- Plantilla HTML única del resumen. Backend Django + API Resend (`RESEND_API_KEY`, `DEFAULT_FROM_EMAIL`).
- Local: backend consola si no hay clave.
- Cron: Railway schedule → `python manage.py enviar_resumenes` semanal.

## UI
- Campana 🔔 con contador de no leídos (Alpine) en el header del dashboard.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,3,4 | `construir_resumen` + `enviar_resumenes` + test |
| CA-2 | integración Resend |
| CA-5 | `notificar` + campana + test |
| CA-6 | ResumenSemanalLog |
