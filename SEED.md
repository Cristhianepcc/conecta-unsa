# Siembra de datos (seed) — CONECTA UNSA

Documenta cómo se puebla la base de datos para que la demo se vea **viva y
realista**: taxonomía, configuración, empresas reales con su logo, convocatorias,
imágenes y cuentas de acceso por rol.

> Todas las cifras de la landing y los dashboards se **calculan** a partir de estos
> datos (nada inflado). La siembra es **idempotente**: se puede correr varias veces
> sin duplicar nada.

---

## TL;DR — sembrar todo

```bash
python manage.py seed_demo
```

Eso orquesta, en orden, todo lo necesario. Para volver a descargar las imágenes:

```bash
python manage.py seed_imagenes --force
```

---

## Comandos

| Comando | Qué hace | Idempotente |
|---|---|---|
| `seed_demo` | **Orquestador.** Llama a todos los de abajo y crea empresas, convocatorias y usuarios de demo. | ✅ |
| `seed_taxonomia` | Áreas (3) · Facultades (16) · Carreras (43) · Grupos afines. | ✅ |
| `seed_config` | Parámetros legales (RMV, topes, plazos) y pesos de transparencia. | ✅ |
| `seed_elegibilidad` | Matriz estado académico × tipo de convocatoria. | ✅ |
| `seed_cuentas` | Una **cuenta de reclutador** (login por email) por cada empresa. | ✅ |
| `seed_imagenes` | Mapea cada empresa a una **empresa real** y descarga su **logo + banner**. | ✅ |
| `seed_notificaciones` | Notificaciones in-app de demo (campana viva: egresado, empresa, admin). | ✅ |

`seed_demo` ejecuta la secuencia completa:

```
seed_taxonomia → seed_config → seed_elegibilidad
   → crea empresas + convocatorias de muestra
   → crea usuarios de demo (egresado, admin)
   → seed_cuentas         (cuentas de empresa, login por email)
   → seed_imagenes        (identidad real + logos + banners)
   → seed_notificaciones  (campana in-app con no leídas)
```

---

## Qué se siembra

| Dato | Cantidad | Notas |
|---|---|---|
| Taxonomía | 3 áreas / 16 facultades / 43 carreras | De `taxonomia-unsa.md` |
| Parámetros legales | 6 | RMV vigente, topes de jornada, plazos |
| Pesos de transparencia | 8 | `modelo-datos.md` §6 |
| Matriz de elegibilidad | 24 reglas | `matching.md` |
| **Empresas** | 9 | **Empresas reales** (ver tabla) con logo, banner y datos completos |
| **Convocatorias** | 20 | Variando tipo, carrera y % de transparencia (semáforo 🟢🟡🔴) |
| **Notificaciones** | ~9 | In-app para egresado (con no leídas), empresa y admin |
| Administrativo | 1+ | Correo en `AdminAllowlist` |

**No se siembran perfiles de egresado** salvo las cuentas de demo: en producción
cada quien entra con su propio correo institucional y completa su perfil.

---

## Empresas (reales)

Para que el demo se vea genuino, cada empresa se mapea a una **empresa real** que
opera en Arequipa / Perú, coherente con el sector de sus convocatorias. La
identidad final (nombre, web, descripción, logo, banner) la fija `seed_imagenes`.

| Empresa | Sector | Dominio del logo | Convocatorias |
|---|---|---|---|
| **Globant** | Software / TI | globant.com | Desarrollo, Backend Python, Trainee Datos, QA |
| **UNACEM** | Construcción / cemento | unacem.pe | Asistente de Obra, Ing. Civil, Arquitectura |
| **Danper** | Agroindustria | danper.com | Ing. Agrónomo, Voluntariado rural |
| **Clínica Internacional** | Salud | clinicainternacional.com.pe | Enfermería, Nutrición |
| **Estudio Echecopar** | Legal | echecopar.com.pe | Abogado corporativo, Consultoría legal |
| **Cerro Verde** | Minería (Arequipa) | cerroverde.pe | Ing. de Minas, Especialista Ambiental |
| **Pronabec** | Becas (Estado) | pronabec.gob.pe | Beca docente, Tutoría |
| **PwC Perú** | Consultoría / finanzas | pwc.com | Marketing, Trainee Finanzas, Contador |
| **Aceros Arequipa** | Industrial (Arequipa) | acerosarequipa.com | (empresa del login `demo_empresa`) |

> ⚠️ **Uso académico / demo.** Los logos y nombres son marcas de sus titulares y se
> usan solo con fines de prototipo no comercial. Esto se aparta a propósito de la
> regla original de `specs/seed-demo.md` ("nombres ficticios"), por decisión del
> equipo para maximizar el realismo de la demostración.

---

## Imágenes (`seed_imagenes`)

Se guardan en `static/img/empresas/` y se sirven vía `STATIC_URL`, de modo que el
render **no depende de la red** (no hay enlaces externos que se rompan).

- **Logo** → `static/img/empresas/<ruc>-logo.svg`
  El logotipo real de la empresa, obtenido eligiendo la **mejor resolución
  disponible** entre varias fuentes (unavatar.io → favicon de Google `sz=256` →
  DuckDuckGo). Se compone sobre una **tarjeta blanca redondeada** (estilo avatar
  de empresa de LinkedIn) y se embebe en **base64 dentro de un SVG** → archivo
  autocontenido y nítido.
- **Banner** → `static/img/empresas/<ruc>-banner.jpg`
  Fotografía sectorial real de Unsplash (tech, construcción, agro, salud, legal,
  minería, educación, consultoría, industrial).

Dónde se muestran:

| Vista | Plantilla | Tamaño del logo |
|---|---|---|
| Landing (destacadas) | `core/home.html` | 56px |
| Feed del egresado | `convocatorias/_tarjeta.html` | 56px |
| Detalle de convocatoria | `convocatorias/detalle.html` | 80px + banner |

Notas de calidad: Globant, Danper, PwC, Echecopar, Pronabec y Clínica Internacional
salen nítidos; Cerro Verde y Aceros Arequipa solo exponen favicons de baja
resolución, así que se ven algo más suaves (se mantienen por ser los referentes de
Arequipa).

---

## Cuentas de acceso (`seed_cuentas`)

Cada empresa "existe" como cuenta para poder probar el flujo de reclutador
(publicar, ver alcance, etc.). El login es por **email + contraseña** (allauth con
`ACCOUNT_LOGIN_METHODS = {"email"}`); cada cuenta registra su `EmailAddress`
verificado para que el login por correo funcione.

**Contraseña común para toda la demo: `demo12345`**

### Empresas (reclutador)

| Empresa | Email de acceso |
|---|---|
| Globant | `talento@globant.com` |
| UNACEM | `seleccion@unacem.pe` |
| Danper | `rrhh@danper.com` |
| Clínica Internacional | `seleccion@clinicainternacional.com.pe` |
| Estudio Echecopar | `reclutamiento@echecopar.com.pe` |
| Cerro Verde | `empleos@cerroverde.pe` |
| Pronabec | `convocatorias@pronabec.gob.pe` |
| PwC Perú | `careers@pwc.pe` |
| Aceros Arequipa | `rrhh@acerosarequipa.com` |

### Otros roles

| Rol | Email | Usuario |
|---|---|---|
| Egresado | `demo.egresado@unsa.edu.pe` | `demo_egresado` |
| Administrativo | `demo.admin@unsa.edu.pe` | `demo_admin` |

> El egresado de demo tiene perfil completo (Ingeniería Industrial, egresado) y
> credenciales de ejemplo para que el matching y la credencial pública se vean.

---

## Notificaciones (`seed_notificaciones`)

Para que la **campana** no salga vacía, se siembran notificaciones in-app:

- **`demo_egresado`** — convocatorias pertinentes (enlazan a su detalle), fecha límite
  próxima, resumen semanal y un aviso general. Mezcla leídas/no leídas → el contador
  de la campana muestra un número.
- **`demo_empresa`** — convocatoria observada + bienvenida.
- **`demo_admin`** — aviso de convocatorias pendientes de revisión.

Los `creado_en` se escalonan (minutos/horas/días atrás) para que el orden cronológico
se vea realista.

---

## Producción

Para desplegar, ver el checklist [`A-PRODUCCION.md`](A-PRODUCCION.md). Punto clave:
las imágenes están **versionadas en el repo** (las sirve WhiteNoise tras
`collectstatic`); en producción `seed_demo` solo rellena la BBDD y **no vuelve a
descargar** los logos.

---

## Detalles de implementación

- Los archivos viven en:
  - `apps/core/management/commands/seed_demo.py` (orquestador)
  - `apps/taxonomia/management/commands/seed_taxonomia.py`
  - `apps/core/management/commands/seed_config.py`
  - `apps/matching/management/commands/seed_elegibilidad.py`
  - `apps/empresas/management/commands/seed_cuentas.py`
  - `apps/empresas/management/commands/seed_imagenes.py`
  - `apps/notificaciones/management/commands/seed_notificaciones.py`
- Las empresas se identifican por **RUC** (clave estable); `seed_imagenes` y
  `seed_cuentas` actualizan la misma empresa por RUC, así que el orden de ejecución
  no genera duplicados.
- `seed_imagenes` solo descarga lo que falta; usa `--force` para rebajar todo.
- Las imágenes descargadas se **versionan** en el repositorio (no están en
  `.gitignore`), de modo que la demo funciona en cualquier clon sin red.

---

## Resolución de problemas

- **Los logos se ven como los antiguos** → caché del navegador. Recarga con
  `Ctrl + Shift + R`.
- **Un logo falla al descargar** (blip de red) → vuelve a correr `seed_imagenes`
  (sin `--force`): solo reintenta lo que falta.
- **No se ve ningún logo en local** → confirma `DEBUG=True` (runserver sirve
  `static/`) o corre `python manage.py collectstatic`.
