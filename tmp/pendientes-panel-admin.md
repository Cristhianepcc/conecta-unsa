# Pendientes — Panel Admin & Notificaciones (UX)

> Archivo temporal de seguimiento. No commitear. Última actualización: 2026-06-14.
> Trabajo ya commiteado en `de7b4d2` (rama `feat/build-conecta-unsa`).

## ✅ Hecho (commit `de7b4d2`)
- **Bandeja** (`panel_admin.html`): métricas agrupadas (cola/salud) clicables, búsqueda
  por título/empresa, chips de filtro con conteos, orden FIFO, aprobar inline, badges
  de estado/transparencia consistentes (reutiliza partials).
- **Revisar** (`revisar.html`): ficha completa (remuneración, vacantes, jornada, fechas,
  no discriminación, medio de postulación, carreras, empresa), comparador de duplicado
  lado a lado, jerarquía de acciones, observar exige comentario, rechazar pide
  confirmación, alerta de incompleta lista los campos faltantes.
- **Navegación**: conserva filtro/búsqueda tras aprobar/observar/rechazar (`next` validado
  con `url_has_allowed_host_and_scheme`).
- **Notificaciones**: campana → dropdown (últimas 5 + "marcar todas como leídas"),
  partial `_fila.html` único, contador "sin leer", cierre con Escape.
- **a11y**: label del buscador, sr-only en "verificada", sin enlaces muertos en dropdown,
  regla CSS `[x-cloak]` (arregla flash del sidebar).

## ⏳ Pendiente — pulido panel admin

| # | Tarea | Esfuerzo |
|---|-------|:--:|
| #9 | Estado de carga / anti doble-clic en "Aprobar" (bandeja inline y revisar). | Bajo |
| #7 | Extraer `_alerta_badge.html` — los 5 badges de alerta están inline/duplicados en `panel_admin.html`. | Bajo |
| #8 | Sidebar admin: reemplazar bloque promocional por mini-resumen de cola ("12 pendientes · 3 duplicados"). | Bajo |
| #13 | Menú en el avatar de la topbar (perfil / cerrar sesión). | Bajo |
| #10 | Paginación + orden configurable en la bandeja (hoy FIFO fijo, scroll infinito). | Medio |
| #14 | "Marcar todas como leídas" asíncrono (hoy recarga toda la página). | Medio |

Recomendación: agrupar #9, #7, #8, #13 en una segunda tanda rápida de pulido.

## 🔵 Pendiente mayor — gap vs. spec `12-panel-admin`
Módulos contemplados en la spec que NO existen (delegados a Django Admin):
- Reportes / métricas de difusión y alcance.
- Control de frecuencia por empresa (panel de saturación).
- Clasificación por categoría.
→ Convierte "moderador de cola" en "panel institucional". Tratar como feature aparte.

## ⚠️ Coordinación (trabajo concurrente, NO mío)
- WIP de datos-demo sin commitear en el working tree: `seed_demo.py`,
  `apps/empresas/management/` (seed_imagenes, seed_cuentas), `static/img/empresas/`.
- El otro flujo rediseñó el **dashboard de empresa** (commit `b46bb80`) y unificó
  `convocatorias/_transparencia.html` con parámetro `variant` (`bar|pill|dot`). Mis
  includes ya usan esa ruta.
- Sin auditar aún: **dashboard de empresa** y **dashboard de egresado**.
