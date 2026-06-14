# Requisitos — 00 Fundación

> Base técnica sobre la que se construye todo. Obedece [`../constitucion.md`](../constitucion.md).

## Objetivo
Dejar el proyecto Django operativo en local y listo para Railway, con la estructura modular,
config por entorno y el patrón config-as-data.

## Alcance
- **Incluye:** proyecto Django, apps vacías, settings 12-factor, Postgres, estáticos, deploy files, locale.
- **No incluye:** lógica de negocio (cada feature la aporta).

## Historias de usuario
- **HU-1:** Como desarrollador, quiero un proyecto Django con apps modulares para construir feature por feature.
- **HU-2:** Como desarrollador, quiero la config por variables de entorno para correr igual en local y Railway.

## Criterios de aceptación (EARS)
- **CA-1:** El sistema debe arrancar con `manage.py runserver` en local usando Python 3.13.
- **CA-2:** El sistema debe leer la base de datos desde `DATABASE_URL` (Postgres) y caer a config local con `.env`.
- **CA-3:** Mientras `DEBUG=False`, el sistema debe servir estáticos con WhiteNoise y exigir `ALLOWED_HOSTS`.
- **CA-4:** El sistema debe operar en `es` / `America/Lima` / `PEN`.
- **CA-5:** El sistema debe incluir las apps: taxonomia, usuarios, empresas, convocatorias, matching, notificaciones, core.
- **CA-6:** El sistema debe exponer las tablas config-as-data (ParametroLegal, PesoTransparencia, ReglaElegibilidad, AdminAllowlist) en Django Admin.

## Dependencias
- Ninguna (es la primera).

## Notas legales / no funcionales
- Cumple NFR-SEC-2/3, NFR-I18N-1, NFR-PERF-1/2 (ver `../requisitos-no-funcionales.md`).
