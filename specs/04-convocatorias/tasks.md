# Tareas — 04 Convocatorias

## Implementación
- [x] T1 — Modelo Convocatoria (Nivel 1/2/3 + estado + transparencia) + migraciones.
- [x] T2 — `campos_requeridos(tipo)` (form dinámico Alpine se arma en 11/12 con estos datos).
- [x] T3 — Servicio `validar_legal` (RMV, jornada, voluntariado) usando ParametroLegal.
- [x] T4 — Servicio `calcular_transparencia` usando PesoTransparencia + etiqueta semáforo.
- [x] T5 — Targeting: M2M carreras_objetivo (compatible con `taxonomia.expandir`).
- [x] T6 — `creada_por` + soporte empresa referencial; checkbox no_discriminacion al publicar.
- [x] T7 — Registrado en Django Admin (creación por admin, fieldsets por nivel, recálculo).

## Pruebas
- [x] T8 — test CA-4: subvención < RMV se bloquea (+ jornada > tope).
- [x] T9 — test CA-5: voluntariado sin remuneración.
- [x] T10 — test CA-6/7: % y etiqueta correctos (sueldo pesa 30%, confidencial no suma).
- [x] T11 — test CA-2: solo Nivel 1 + no discriminación (CA-10) permiten publicar.
- [x] CA-1 (8 tipos), CA-3 (campos por tipo), CA-8 (targeting), CA-9 (origen/referencial).

## Cierre
- [x] DoD cumplido — 16 tests EARS verdes.

> Notas:
> - Config-as-data: RMV/topes desde ParametroLegal, pesos desde PesoTransparencia.
>   Comando `seed_config` (en core) siembra ambos. La matriz de elegibilidad la siembra 05.
> - `publicar()` valida Nivel 1 + no discriminación + legalidad y deja la convocatoria en `pendiente`.
