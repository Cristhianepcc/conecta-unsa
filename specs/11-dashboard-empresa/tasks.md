# Tareas — 11 Dashboard Empresa

## Implementación
- [x] T1 — Vistas con guard `empresa_required` + helper `empresa_de(usuario)`.
- [x] T2 — Inicio `/empresas/dashboard`: métricas propias calculadas (activas, alcance, vistas, publicadas).
- [x] T3 — "Mis convocatorias": tabla con estado, transparencia y acción (editar/corregir).
- [x] T4 — `/empresas/publicar`: formulario dinámico de 3 bloques (`04`) + semáforo (`06`).
- [x] T5 — Vista "corregir observada" (muestra comentario, edita y reenvía).
- [x] T6 — Dashboard limitado si empresa **no verificada** (no puede publicar).
- [x] T7 — Bloque "Estado de tu empresa" + guías de buenas prácticas (mejora progresiva).

## Pruebas
- [x] T8 — test CA-3: no verificada → dashboard limitado y publicar rebota.
- [x] T9 — test CA-4: observada se corrige y vuelve a revisión (+ muestra comentario).
- [x] T10 — test CA-5: métricas calculadas de datos reales.
- [x] CA-2 (publicar crea convocatoria; auto-publica si verificada + 🟢).

## Cierre
- [x] DoD cumplido — 7 tests EARS verdes.

> Nota: al publicar/corregir se valida Nivel 1 + legalidad y se aplica el semáforo de confianza
> (06): empresa verificada + sin alertas + 🟢 → auto-publicada; si no, pendiente de revisión.
> `ConvocatoriaForm` excluye empresa/creada_por/estado (los fija la vista).
