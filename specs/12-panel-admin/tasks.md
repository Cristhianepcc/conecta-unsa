# Tareas — 12 Panel Admin

## Implementación
- [x] T1 — Vista `/panel-admin` (template a medida) con `admin_required`.
- [x] T2 — Tarjetas de métricas superiores reales (recibidas, validadas, pendientes, duplicados, transparencia).
- [x] T3 — Bandeja de convocatorias con badges de alerta + semáforo (de `06`).
- [x] T4 — Acciones aprobar / observar (comentario) / rechazar (`/panel-admin/convocatoria/<id>`).
- [x] T5 — Resaltar duplicados con % de similitud.
- [x] T6 — Paneles de métricas / nota a reportes (Django Admin para CRUD).
- [x] T7 — Django Admin ya cubre config-as-data + empresas/convocatorias referenciales.

## Pruebas
- [x] T8 — test CA-6: no-admin no entra al panel (403); admin sí.
- [x] T9 — test CA-2: aprobar/observar(comentario+notifica)/rechazar; observar sin comentario no procede.
- [x] T10 — test CA-4: métricas calculadas de datos reales.
- [x] CA-1 (bandeja con transparencia), CA-3 (resalta duplicado con % similitud).

## Cierre
- [x] DoD cumplido — 9 tests EARS verdes.

> Nota: panel híbrido — bandeja y métricas en template a medida; el CRUD pesado y la
> configuración (ParametroLegal, PesoTransparencia, ReglaElegibilidad, taxonomía, empresas
> referenciales) en Django Admin (`/admin/`). Las acciones reutilizan el flujo de 06.
