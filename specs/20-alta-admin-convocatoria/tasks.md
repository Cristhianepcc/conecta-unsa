# Tareas — 20 Alta de convocatoria por el administrativo

> Deriva de `design.md`.

## Implementación
- [ ] T1 — Variante de `ConvocatoriaForm` (o flag) con campo `empresa` visible para admin.
- [ ] T2 — Vista `core.crear_convocatoria` con `admin_required` (GET/POST).
- [ ] T3 — Al guardar: `creada_por = CREADA_POR_ADMIN` + estado inicial según flujo.
- [ ] T4 — Ruta `panel-admin/convocatoria/nueva/` + botón "Registrar convocatoria recibida".
- [ ] T5 — Reusar `_form.html` con selector de empresa.

## Datos / seed
- [ ] T6 — (sin seed nuevo)

## Pruebas (criterios EARS → tests)
- [ ] T7 — test CA-1/CA-2: admin crea convocatoria → existe con `creada_por=admin` y la empresa elegida.
- [ ] T8 — test CA-3: la convocatoria admin dispara faltantes/duplicados igual que una de empresa.
- [ ] T9 — test CA-4: rol no admin → 403.

## Cierre
- [ ] Sin migraciones (no cambia el modelo).
- [ ] Definition of Done de la constitución cumplido.
