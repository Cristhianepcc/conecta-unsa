# Tareas — 04 Convocatorias

## Implementación
- [ ] T1 — App `convocatorias`; modelo Convocatoria (Nivel 1/2/3 + estado + transparencia) + migraciones.
- [ ] T2 — `campos_requeridos(tipo)` y formulario dinámico (Alpine, 3 bloques).
- [ ] T3 — Servicio `validar_legal` (RMV, jornada, voluntariado) usando ParametroLegal.
- [ ] T4 — Servicio `calcular_transparencia` usando PesoTransparencia + etiqueta semáforo.
- [ ] T5 — Targeting: M2M carreras_objetivo vía `taxonomia.expandir`.
- [ ] T6 — `creada_por` + soporte empresa referencial; checkbox no_discriminacion al publicar.
- [ ] T7 — Registrar en Django Admin (para creación por admin).

## Pruebas
- [ ] T8 — test CA-4: subvención < RMV se bloquea/advierte.
- [ ] T9 — test CA-5: voluntariado sin remuneración.
- [ ] T10 — test CA-6/7: % y etiqueta correctos (sueldo pesa 30%).
- [ ] T11 — test CA-2: solo Nivel 1 permite publicar.

## Cierre
- [ ] DoD cumplido.
