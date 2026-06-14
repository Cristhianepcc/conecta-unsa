# Tareas — 07 Perfil y Credencial

## Implementación
- [x] T1 — Modelos PerfilTalento, Credencial + migraciones.
- [x] T2 — `/completar-perfil` (carrera + estado + consentimiento en primer ingreso).
- [x] T3 — `/perfil`: alta/edición de credenciales autodeclaradas; verificadas solo lectura (badge 🟢).
- [x] T4 — Preferencias (carreras extra, silenciar, tipos, frecuencia semanal por defecto).
- [x] T5 — Credencial pública: activar/revocar, slug único, control de visibilidad.
- [x] T6 — Página `/credencial/<slug>` solo lectura + `noindex` (meta + X-Robots-Tag) + sin features sociales.

## Pruebas
- [x] T7 — test CA-3: credencial verificada no editable por el egresado.
- [x] T8 — test CA-5/6: activar genera URL; sirve con noindex.
- [x] T9 — test CA-7: revocar apaga la URL (404).
- [x] CA-1 (carrera+estado), CA-2 (autodeclaradas), CA-4 (preferencias).

## Cierre
- [x] DoD cumplido — 7 criterios EARS verdes (clase PerfilTalentoTests).

> Notas:
> - PerfilTalento es 1-1 con User (separado de Perfil de 02: rol/consent). Lleva carrera +
>   estado_academico (lo que el matching usa en Gate 1/2) + credenciales (Layer 3).
> - TODO producción: carrera/estado/credenciales verificadas llegan por sync y son solo lectura.
> - Orden: 07 se construyó antes de 05 por dependencia (matching necesita el perfil).
> - La URL pública queda en `/usuarios/credencial/<slug>/` (apps montadas con prefijo en 00).
