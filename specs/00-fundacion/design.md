# Diseño — 00 Fundación

## Estructura
```
conecta_unsa/        settings.py (env), urls.py, wsgi.py
apps/
  core/              ParametroLegal, PesoTransparencia, ReglaElegibilidad, AdminAllowlist; base templates
  taxonomia/ usuarios/ empresas/ convocatorias/ matching/ notificaciones/   (vacías al inicio)
templates/ static/
manage.py · requirements.txt · .python-version (3.13) · runtime.txt
Procfile / railway.json · docker-compose.yml · .env.example · .gitignore
```

## Settings (12-factor)
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` desde entorno.
- `DATABASES` vía `dj-database-url` (`DATABASE_URL`); fallback `.env` local.
- `STATICFILES_STORAGE` = WhiteNoise comprimido.
- `LANGUAGE_CODE='es'`, `TIME_ZONE='America/Lima'`, `USE_TZ=True`.
- `django-allauth` preinstalado (se configura en `02`).

## requirements.txt (base)
`Django` · `gunicorn` · `psycopg[binary]` · `dj-database-url` · `whitenoise` · `django-allauth` · `resend` · `python-dotenv` · `pytest-django`.

## Deploy
- `Procfile`: `web: gunicorn conecta_unsa.wsgi` + release: `migrate` y `collectstatic`.
- Extensión `pg_trgm`: migración `CREATE EXTENSION IF NOT EXISTS pg_trgm` (la usa `06`).

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1..4 | settings + .python-version + runtime |
| CA-5 | apps creadas en INSTALLED_APPS |
| CA-6 | modelos `core` + Django Admin |
