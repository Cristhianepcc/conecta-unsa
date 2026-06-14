# Despliegue — CONECTA UNSA

> **Trabajamos en local primero.** El despliegue lo hace el usuario **manualmente**:
> se crea el repo, se conecta a Railway, se configuran las variables de entorno.
> El asistente prepara todo lo necesario y **entrega la lista de variables**; no despliega.

---

## 1. Flujo de despliegue (manual)

1. Desarrollo y pruebas en **local**.
2. Se crea el **repositorio** y se sube el código.
3. El usuario **conecta el repo a Railway** (plan **Hobby**).
4. Se agrega el **PostgreSQL administrado de Railway** (plugin) → inyecta `DATABASE_URL`.
5. El usuario **configura las variables de entorno** (lista en §4) en Railway.
6. Se apunta el dominio **`grellox.com`** al servicio (custom domain de Railway).

> Contexto: es una **presentación de MVP** — el objetivo es **mostrar la funcionalidad**,
> no una operación de producción real.

---

## 2. Base de datos

- **PostgreSQL administrado en Railway** (plugin). Railway provee `DATABASE_URL`.
- En local: PostgreSQL vía `docker-compose` (coincide con prod) — ver `stack-conecta-unsa.md`.

---

## 3. Configuración de la app para Railway

- **Python 3.13** (fijado en local y en Railway con `.python-version` / `runtime.txt`).
  No se usa 3.14 (demasiado nuevo: Django/`psycopg` aún no garantizan compatibilidad).
- **Gunicorn** como servidor WSGI.
- **WhiteNoise** para servir estáticos (sin Nginx aparte en Railway).
- `dj-database-url` para leer `DATABASE_URL`.
- `Procfile` o `railway.json` con el comando de arranque + `migrate` + `collectstatic`.
- `requirements.txt`: Django, gunicorn, psycopg2-binary, dj-database-url, whitenoise, resend, python-dotenv.

---

## 4. Variables de entorno (el usuario las configura en Railway)

El asistente **entregará estos valores** al momento del deploy; el usuario los pega en Railway:

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django (se genera) |
| `DEBUG` | `False` en producción |
| `ALLOWED_HOSTS` | `grellox.com`, dominio de Railway |
| `CSRF_TRUSTED_ORIGINS` | `https://grellox.com` |
| `DATABASE_URL` | La inyecta Railway (Postgres administrado) |
| `RESEND_API_KEY` | Clave de Resend (correo) |
| `DEFAULT_FROM_EMAIL` | Remitente verificado en Resend (dominio de prueba) |

En **local** se usa un `.env` (no versionado) con valores de desarrollo
(`DEBUG=True`, base local, sin envío real de correo si se desea).

---

## 5. Dominio

- Producción del MVP: **`grellox.com`** (custom domain en Railway).
- Proyecto Railway: **conecta-unsa**.
