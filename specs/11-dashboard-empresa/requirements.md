# Requisitos — 11 Dashboard Empresa

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: `paginas/dashboard empresa.png`, [`../../modelo-datos.md`](../../modelo-datos.md).

## Objetivo
Panel donde la empresa publica y gestiona sus convocatorias, ve su estado/transparencia/alcance,
y corrige las observadas.

## Alcance
- **Incluye:** inicio con métricas propias, lista "Mis convocatorias", **form de publicar** (3 bloques), corregir observada, estado de empresa, dashboard limitado si no verificada.
- **No incluye:** matching interno (`05`), revisión (`06`).

## Historias de usuario
- **HU-1:** Como empresa, quiero publicar una convocatoria con formulario que se adapta a su tipo.
- **HU-2:** Como empresa, quiero ver el estado, transparencia y alcance de mis convocatorias.
- **HU-3:** Como empresa, quiero corregir una convocatoria observada con el comentario del admin.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe listar las convocatorias de la empresa con estado, % completitud/transparencia y alcance (egresados).
- **CA-2:** El sistema debe ofrecer el **formulario de publicar** dinámico de 3 bloques (`04`), con barra de transparencia en vivo.
- **CA-3:** Mientras la empresa esté **no verificada**, el sistema debe mostrar un dashboard **limitado** (sin publicar).
- **CA-4:** Cuando una convocatoria está **observada**, el sistema debe mostrar el comentario y permitir **corregir y reenviar**.
- **CA-5:** El sistema debe mostrar métricas propias (publicaciones activas, alcance, vistas) **calculadas de datos reales**.
- **CA-6:** El sistema debe mostrar el **estado de la empresa** y guías de buenas prácticas (mejora progresiva).

## Dependencias
- `03-empresas`, `04-convocatorias`, `06-flujo-admin`, `05-matching` (alcance).

## Notas
- Métricas honestas (NFR). Logos por URL.
