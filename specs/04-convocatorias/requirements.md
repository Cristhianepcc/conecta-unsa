# Requisitos — 04 Convocatorias

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../modelo-datos.md`](../../modelo-datos.md).

## Objetivo
Modelar la convocatoria (8 tipos), su formulario dinámico de 3 niveles, las validaciones legales
y el cálculo de transparencia.

## Alcance
- **Incluye:** Convocatoria, 8 tipos, campos por nivel, validación legal por tipo, estados, cálculo de transparencia, carreras objetivo, creada_por (empresa/admin).
- **No incluye:** matching/difusión (`05`), revisión admin/alertas (`06`), UI dashboards (`11`,`12`).

## Historias de usuario
- **HU-1:** Como empresa, quiero publicar una convocatoria con lo esencial y completar más para ganar visibilidad.
- **HU-2:** Como empresa, quiero que el formulario me pida solo lo que aplica a mi tipo de convocatoria.
- **HU-3:** Como sistema, quiero calcular el % de transparencia para ordenar la difusión.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe soportar los **8 tipos** de convocatoria.
- **CA-2:** Cuando se completan los **campos Nivel 1**, el sistema debe permitir publicar (estado pendiente).
- **CA-3:** Donde el tipo lo exija, el sistema debe requerir los campos Nivel 2 (ej. convenio en práctica preprofesional, régimen en empleo).
- **CA-4:** Si una subvención/remuneración es menor a la RMV (de `ParametroLegal`), entonces el sistema debe advertir/bloquear según el tipo.
- **CA-5:** Si el tipo es Voluntariado, entonces el sistema debe impedir cargar remuneración.
- **CA-6:** El sistema debe calcular `transparencia_pct` con los `PesoTransparencia` configurables (sueldo 30%).
- **CA-7:** El sistema debe asignar la etiqueta 🟢≥80 / 🟡50–79 / 🔴<50 según el %.
- **CA-8:** El sistema debe asociar la convocatoria a un conjunto de **carreras objetivo** (vía `taxonomia.expandir`).
- **CA-9:** El sistema debe registrar `creada_por` (empresa o admin) y soportar empresa referencial.
- **CA-10:** Cuando la convocatoria se publica, el sistema debe exigir el checkbox de **no discriminación** (Ley 26772).

## Dependencias
- `01-taxonomia` (carreras objetivo), `03-empresas`, `00` (ParametroLegal, PesoTransparencia).

## Notas legales / no funcionales
- Leyes 31572, 30709, 26772 (ver `../../modelo-datos.md`).
