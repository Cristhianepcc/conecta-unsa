# Constitución — CONECTA UNSA (Spec-Driven Development)

> Fuente de verdad del proyecto. Toda spec de feature **obedece** esta constitución y
> **referencia** (no duplica) los documentos de planificación de la raíz.

---

## 1. Principios inviolables

1. **Sin IA** — toda lógica es por reglas transparentes y auditables.
2. **Configuración-como-datos** — taxonomía, matriz de elegibilidad, pesos de transparencia,
   parámetros legales y allowlist viven en **tablas editables por el admin**, no en código.
3. **Software público** — open source, sin proveedores externos atados, datos bajo control institucional.
4. **Mínima fricción + mejora progresiva** — publicar con lo esencial; completar da más visibilidad.
5. **Cumplimiento legal peruano** — Ley 31572, 30709, 29733, 26772, 29973 (ver docs).
6. **Mantenible por equipo pequeño** — monolito modular Django, server-rendered, sin build de Node.

## 2. Stack y arquitectura (canónico)

- Django (Python **3.13**) · PostgreSQL (+`pg_trgm`) · Templates + Tailwind + Alpine (CDN).
- `django-allauth` (Google OAuth) + Django auth (empresa).
- Cron + `manage.py` + Resend (sin Celery/Redis).
- Deploy: Railway (manual) · Gunicorn · WhiteNoise · 12-factor.
- Detalle y justificación: [`../arquitectura.md`](../arquitectura.md).

## 3. Documentos de referencia (capa de decisiones)

| Tema | Doc |
|---|---|
| Problema / propuesta | [`../propuesta.md`](../propuesta.md) |
| Stack | [`../stack-conecta-unsa.md`](../stack-conecta-unsa.md) |
| Arquitectura (ADR) | [`../arquitectura.md`](../arquitectura.md) |
| Taxonomía UNSA | [`../taxonomia-unsa.md`](../taxonomia-unsa.md) |
| Modelo de convocatoria | [`../modelo-datos.md`](../modelo-datos.md) |
| Matching | [`../matching.md`](../matching.md) |
| Flujo admin | [`../flujo-admin.md`](../flujo-admin.md) |
| Auth y roles | [`../auth-roles.md`](../auth-roles.md) |
| Perfil / preferencias | [`../perfil-preferencias.md`](../perfil-preferencias.md) |
| Notificaciones | [`../notificaciones.md`](../notificaciones.md) |
| Branding | [`../branding.md`](../branding.md) |
| Auditoría landing | [`../landing-audit.md`](../landing-audit.md) |
| Deploy | [`../deploy.md`](../deploy.md) |

## 4. Specs transversales (aplican a todas las features)

- [`glosario.md`](glosario.md) — lenguaje ubicuo del dominio.
- [`modelo-datos.md`](modelo-datos.md) — esquema canónico de entidades compartidas.
- [`requisitos-no-funcionales.md`](requisitos-no-funcionales.md) — seguridad, privacidad, WCAG AA, i18n, performance.
- [`estrategia-pruebas.md`](estrategia-pruebas.md) — cómo cada criterio EARS se vuelve test.
- [`seed-demo.md`](seed-demo.md) — datos sembrados para la demo.

## 5. Convención de specs (EARS)

Cada feature = carpeta con `requirements.md`, `design.md`, `tasks.md` (ver [`_template/`](_template/)).

Los criterios de aceptación se escriben en **EARS** (verificables → cada uno es un test):
- **Ubicuo:** "El sistema debe <respuesta>."
- **Evento:** "**Cuando** <disparador>, el sistema debe <respuesta>."
- **Estado:** "**Mientras** <estado>, el sistema debe <respuesta>."
- **Opcional:** "**Donde** <feature incluida>, el sistema debe <respuesta>."
- **No deseado:** "**Si** <condición>, **entonces** el sistema debe <respuesta>."

## 6. Orden de ejecución (dependencias)

```
00-fundacion → 01-taxonomia → 02-autenticacion → 03-empresas → 04-convocatorias
→ 05-matching → 06-flujo-admin → 07-perfil-credencial → 08-notificaciones
→ 09-landing → 10-dashboard-estudiante → 11-dashboard-empresa → 12-panel-admin
```

## 7. Definition of Done (por feature)

- [ ] `requirements.md` con criterios EARS aprobados.
- [ ] `design.md` coherente con el modelo de datos canónico.
- [ ] `tasks.md` completado.
- [ ] Tests de los criterios EARS críticos pasan.
- [ ] Sin secretos en el repo; cambios reflejados en migraciones.
