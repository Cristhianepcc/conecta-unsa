# Checklist — Subir a producción

> Lista accionable de lo que hay que hacer **antes y después** de desplegar en Railway.
> El **cómo** del despliegue (Railway, dominio, lista completa de env vars) está en
> [`deploy.md`](deploy.md); este archivo es el **checklist operativo** que lo complementa.

---

## 1. Antes de desplegar (en el repo)

- [ ] **Commitear todo el trabajo de la siembra.** En especial:
  - `static/img/empresas/*.svg` y `*.jpg` (logos y banners) — **deben estar versionados**
    (no en `.gitignore`), porque `collectstatic` los recoge en el build y WhiteNoise los
    sirve. Si no se commitean, en producción no se verá ninguna imagen.
  - Los comandos nuevos: `seed_cuentas.py`, `seed_imagenes.py`, `seed_notificaciones.py`.
  - Docs: [`SEED.md`](SEED.md), este archivo.
- [ ] **`DEBUG=False`** y `ALLOWED_HOSTS` con el dominio real (`grellox.com` + dominio de Railway).
- [ ] **`SECRET_KEY`** de producción (generada, no la de desarrollo).
- [ ] Revisar `requirements.txt` y `runtime.txt` (Python 3.13, no 3.14).

## 2. Variables de entorno (Railway)

Ver la tabla completa en [`deploy.md`](deploy.md) §4. Mínimo imprescindible:

- [ ] `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
- [ ] `DATABASE_URL` — la inyecta el plugin de PostgreSQL de Railway (no se pone a mano)
- [ ] `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` (OAuth)
- [ ] `RESEND_API_KEY` + `DEFAULT_FROM_EMAIL` (correo del resumen semanal)

## 3. Lo que ya está automatizado (no tocar)

`railway.json` ya ejecuta:
- **Build:** `python manage.py collectstatic --noinput` → recoge `static/` (incluidas las
  imágenes de empresas) a `STATIC_ROOT`; WhiteNoise las sirve.
- **preDeploy:** `python manage.py migrate --noinput`.

## 4. Después del primer deploy — SEMBRAR LA BBDD ⚠️

`migrate` crea las tablas **vacías**. Hay que sembrar los datos **una vez** (comando
único de Railway o consola del servicio):

```bash
python manage.py seed_demo
```

Esto deja la demo lista: taxonomía, config, 9 empresas reales con logo/banner,
20 convocatorias, cuentas de empresa, usuarios de demo y **notificaciones**.
Es **idempotente** → se puede volver a correr sin duplicar nada.
Detalle completo en [`SEED.md`](SEED.md).

> **Importante sobre las imágenes en prod:** el FS de Railway es **efímero**. Los logos
> y banners NO se descargan en producción: están **versionados en el repo** y servidos
> por WhiteNoise tras `collectstatic`. Al correr `seed_demo` en prod, `seed_imagenes`
> encuentra los archivos ya presentes y **solo rellena la BBDD** (no vuelve a descargar).
> Si algún día se borran del repo, habría que regenerarlos en local con
> `python manage.py seed_imagenes --force` y volver a commitear.

## 5. Configuración de identidad / OAuth

- [ ] **Google OAuth:** registrar la **URL de callback** del dominio de producción en la
  consola de Google Cloud (`https://grellox.com/accounts/google/login/callback/`).
- [ ] **Django Sites:** el `Site` (id=1) debe tener el **dominio de producción** (allauth lo usa
  para construir URLs). Ajustar en el admin o por data migration.
- [ ] **`AdminAllowlist`:** confirmar que los correos institucionales que deben ser admin
  están en la allowlist (el rol admin se otorga por correo, no por elección).

## 6. Seguridad / limpieza para una prod real

> Para la **demo de hackathon** se puede dejar tal cual. Para una operación real:

- [ ] **Deshabilitar o quitar las cuentas de demo** (`demo_*`) y los usuarios de prueba
  (`dev_*`, `empresa1`) — todas usan la contraseña pública `demo12345`.
- [ ] No sembrar datos de demo en la BBDD real (correr solo `seed_taxonomia` + `seed_config`
  + `seed_elegibilidad`, sin `seed_demo`).
- [ ] Revisar que el envío de correo (Resend) use un dominio remitente verificado.

---

## Nota sobre la siembra (resumen)

La demo se puebla con `python manage.py seed_demo`, que encadena:

```
seed_taxonomia → seed_config → seed_elegibilidad
   → empresas + convocatorias de muestra → usuarios de demo
   → seed_cuentas (logins de empresa por email)
   → seed_imagenes (empresas reales + logos/banners, versionados)
   → seed_notificaciones (campana in-app)
```

- **Empresas reales** (Globant, UNACEM, Danper, Clínica Internacional, Estudio Echecopar,
  Cerro Verde, Pronabec, PwC Perú, Aceros Arequipa) con logo real + banner sectorial.
- **Credenciales de demo** y detalle de cada comando: ver [`SEED.md`](SEED.md).
- **Notificaciones** sembradas para `demo_egresado` (campana con no leídas), `demo_empresa`
  y `demo_admin`.
- **Salvedad:** los logos de Cerro Verde y Aceros Arequipa son de baja resolución (favicons),
  se ven algo suaves; el resto sale nítido.
