# Tareas — 03 Empresas

## Implementación
- [x] T1 — Modelos Empresa, Reclutador + migraciones.
- [x] T2 — Properties `es_referencial`, `verificada` (+ `puede_publicar`).
- [x] T3 — Vista/form de registro (paso RUC + bloque A empresa + bloque B reclutador).
- [x] T4 — Validación: RUC único (CA-7), logo/banner como URL (CA-6).
- [x] T5 — Django Admin: acciones activar/rechazar; crear empresa referencial (inline reclutador).
- [x] T6 — Guard reutilizable `empresa_puede_publicar()` (estado activa).

## Pruebas
- [x] T7 — test CA-1/CA-2: registro crea pendiente; pendiente no publica.
- [x] T8 — test CA-3: activar → verificada y puede publicar.
- [x] T9 — test CA-4: empresa referencial sin badge.
- [x] T10 — test CA-7: RUC duplicado rechazado (+ usuario duplicado, CA-5 OneToOne).

## Cierre
- [x] DoD cumplido — 8 tests EARS verdes.

> Nota: el registro crea el User (rol=reclutador), la Empresa (pendiente) y el Reclutador
> en una transacción. La vista placeholder de la feature 02 quedó reemplazada por el form real.
