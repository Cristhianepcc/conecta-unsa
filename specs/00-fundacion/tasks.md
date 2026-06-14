# Tareas — 00 Fundación

## Implementación
- [x] T1 — `django-admin startproject conecta_unsa` + carpeta `apps/`.
- [x] T2 — Crear apps: core, taxonomia, usuarios, empresas, convocatorias, matching, notificaciones.
- [x] T3 — settings 12-factor (env vars, dj-database-url, WhiteNoise, allauth, locale es/Lima/PEN).
- [x] T4 — Modelos config-as-data en `core` (ParametroLegal, PesoTransparencia, ReglaElegibilidad, AdminAllowlist) + admin.
- [x] T5 — `requirements.txt`, `.python-version` (3.13), `runtime.txt`.
- [x] T6 — `Procfile`/`railway.json`, `docker-compose.yml` (local: web+postgres), `.env.example`, `.gitignore`.
- [x] T7 — Migración `CREATE EXTENSION pg_trgm`.

## Pruebas
- [x] T8 — test CA-1: el proyecto arranca y responde 200 en `/`.
- [x] T9 — test CA-2: lee `DATABASE_URL`.

## Cierre
- [x] `migrate` ok · `runserver` ok · DoD cumplido.

> Notas:
> - Stack real: Django 6.0.6 sobre Python 3.14 local (3.13 es el contrato de deploy en
>   `.python-version`/`runtime.txt`; Django 6.x es compatible con ambas). Único desvío del entorno.
> - Constantes canónicas centralizadas en `apps/core/constants.py` (estados académicos, tipos de
>   convocatoria, criterios de transparencia, parámetros legales base) para que las features no dupliquen.
> - Tests: 6 criterios verdes (CA-1, CA-2, CA-4, CA-5, CA-6).
