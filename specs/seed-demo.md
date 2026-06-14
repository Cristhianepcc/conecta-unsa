# Seed de Demo

> Datos que se siembran para que la demo se vea viva. Cruza varias features → spec transversal.
> Las cifras de la landing/dashboards se **calculan** de estos datos (nada inflado — ver `../landing-audit.md`).

## Qué se siembra
| Dato | Cantidad | Notas |
|---|---|---|
| Taxonomía completa | 3 áreas / 16 facultades / 43 carreras | De `../taxonomia-unsa.md` |
| GrupoAfin base | 3–5 | "Administración o afines", "Ingenierías o afines", "Salud o afines"… |
| Parámetros legales | varios | RMV vigente, topes de jornada, plazos |
| Pesos de transparencia | 8 | Según `../modelo-datos.md` §6 |
| Matriz de elegibilidad | filas estado×tipo | Según `../matching.md` |
| **Empresas de muestra** | ~8 | **Ficticias realistas** (ej. "Altiplano Tech SAC", "Constructora del Misti") — mezcla registradas y referenciales |
| **Convocatorias de muestra** | **15–25** | Repartidas por tipos, carreras y niveles de transparencia |
| 1 administrativo | 1 | Correo en `AdminAllowlist` (para la demo) |

## Qué NO se siembra
- **Perfiles de estudiante/egresado:** cada quien entra con su **propio Gmail** y completa su perfil.
  El presentador usa 2–3 cuentas Gmail propias con estados distintos para mostrar el matching.

## Reglas
- Las convocatorias de muestra deben cubrir: varios **tipos** (práctica, empleo, CAS, voluntariado…),
  varias **carreras/áreas**, y un **rango de % de transparencia** (alta 🟢, media 🟡, baja 🔴)
  para que el semáforo se vea.
- Empresas: **nombres ficticios** (no usar empresas reales sin autorización).
- Implementación: comando `manage.py seed_demo` idempotente.
