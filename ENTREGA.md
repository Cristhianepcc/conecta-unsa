# CONECTA UNSA — Reporte de Implementación

Bolsa de Trabajo de la UNSA construida por Spec-Driven Development (MODO B, secuencial)
siguiendo `specs/`. Todas las features (00→12) están implementadas con sus criterios EARS en verde.

## Estado: ✅ completo

| # | Feature | Tests EARS |
|---|---------|:--:|
| 00 | Fundación (Django, apps, settings 12-factor, config-as-data) | 6 |
| 01 | Taxonomía (Área/Facultad/Carrera/GrupoAfin, `expandir`, seed 3/16/43) | 11 |
| 02 | Autenticación (2 puertas Google/empresa, ruteo por rol, consentimiento) | 15 |
| 03 | Empresas (registro RUC, estados, badge verificada, referencial) | 8 |
| 04 | Convocatorias (8 tipos, 3 niveles, validación legal, transparencia) | 16 |
| 05 | Matching (elegibilidad/carrera/ranking explicable, sin IA) | 10 |
| 06 | Flujo admin (estados, alertas, duplicados pg_trgm, semáforo, caducidad) | 13 |
| 07 | Perfil y credencial (PerfilTalento, credenciales, credencial pública opt-in) | 7 |
| 08 | Notificaciones (resumen semanal Resend, campana in-app) | 9 |
| 09 | Landing (métricas honestas, categorías reales, footer legal) | 7 |
| 10 | Dashboard estudiante (feed, detalle, postular, guardadas, historial) | 6 |
| 11 | Dashboard empresa (publicar, métricas, corregir observada) | 7 |
| 12 | Panel admin (bandeja con alertas, aprobar/observar/rechazar, métricas) | 9 |
| | **Total** | **123** |

Ejecutar la suite: `pytest` (todo verde). Cobertura: lógica de servicios, reglas de acceso por
rol, integridad de datos y flujos clave (estrategia-pruebas.md).

## Cómo correr en local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # ajusta DATABASE_URL si hace falta
createdb conecta_unsa         # PostgreSQL con extensión pg_trgm (la crea la migración)
python manage.py migrate
python manage.py seed_demo    # taxonomía + config + 8 empresas + 20 convocatorias (idempotente)
python manage.py createsuperuser
python manage.py runserver
```

- Landing: `/` · Login (2 puertas): `/usuarios/login/` · Registro empresa: `/empresas/registro/`
- Panel admin a medida: `/panel-admin/` (rol admin por allowlist) · Django Admin: `/admin/`
- Cron semanal (Railway): `python manage.py enviar_resumenes` — schedule sugerido `0 8 * * 1` (lunes 08:00)
- Caducidad diaria (Railway): `python manage.py caducar_vencidas` — schedule sugerido `0 3 * * *` (03:00 diario)

  > Se configuran como **servicios cron** en el dashboard de Railway apuntando al mismo deploy
  > (no van en `railway.json`). Aun si el cron de caducidad fallara, el feed y el resumen ya
  > excluyen vencidas por código (`matching.convocatorias_publicadas`, feature 13).

## Comandos de gestión
`seed_demo` (todo), `seed_taxonomia`, `seed_config`, `seed_elegibilidad`,
`enviar_resumenes`, `caducar_vencidas`.

## Pendientes que aporta el usuario (fuera del código)
- 🖼️ **Escudo UNSA oficial** (SVG/PNG) → reemplaza el placeholder del header (`templates/base.html`).
- 🔑 **GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET** (OAuth de Google) para la puerta UNSA.
- 🔑 **RESEND_API_KEY + dominio remitente** (verificar SPF/DKIM en Resend) para el correo real.
- 👥 **Nombres de los 4 integrantes** (solo para el PDF de entrega; no van en el código).

## Variables de entorno (Railway)
```
SECRET_KEY=<clave-larga-aleatoria>
DEBUG=False
ALLOWED_HOSTS=<tu-dominio>,.railway.app
CSRF_TRUSTED_ORIGINS=https://<tu-dominio>,https://*.railway.app
DATABASE_URL=<postgres de Railway>      # con pg_trgm
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
RESEND_API_KEY=...                       # activa envío por SMTP de Resend
DEFAULT_FROM_EMAIL=CONECTA UNSA <no-reply@tu-dominio>
```
Deploy: `Procfile` / `railway.json` (release ejecuta `migrate` + `collectstatic`; web con Gunicorn + WhiteNoise).

## Desvíos registrados (decisiones de implementación)
- **Python**: el contrato de deploy es 3.13 (`.python-version`/`runtime.txt`); el venv local usa
  **3.14** (único disponible) con **Django 6.0** (compatible con ambas).
- **Taxonomía**: la fuente tenía 17 fac/47 carreras en el detalle; por decisión del usuario se
  ajustó al conteo canónico **3/16/43** (config-as-data, editable en el admin). Detalle en
  `specs/01-taxonomia/tasks.md`.
- **Orden**: `07-perfil-credencial` se construyó antes de `05-matching` por dependencia real
  (el matching necesita carrera/estado/credenciales del perfil).

## Próximos pasos sugeridos (post-MVP)
- Restringir Google a `@unsa.edu.pe` (`hd=unsa.edu.pe`) en `SOCIALACCOUNT_PROVIDERS` (TODO ya marcado).
- Sync institucional real para credenciales verificadas (hoy todo autodeclarado en demo).
- Estados de posgrado (Magíster/Doctor): ya escala solo agregando filas a `ReglaElegibilidad`.
