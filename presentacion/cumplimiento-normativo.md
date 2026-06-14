# Cumplimiento de lineamientos del Estado peruano — CONECTA UNSA

> **Propósito.** Responder, dimensión por dimensión, a los lineamientos oficiales del
> Estado peruano aplicables a un sistema web institucional, indicando qué cumple el
> prototipo, con qué evidencia en el código, y qué queda como trabajo futuro.

**Proyecto:** CONECTA UNSA — bolsa de trabajo institucional para estudiantes y egresados
de la Universidad Nacional de San Agustín de Arequipa y empresas verificadas.
**Stack:** Django 6 + PostgreSQL + Gunicorn + WhiteNoise · Tailwind CSS + Alpine.js (server-rendered).

---

## Resumen ejecutivo

| # | Dimensión | Estado | Síntesis |
|---|-----------|--------|----------|
| 1 | Identidad visual y diseño | 🟢 Cumple | Sistema de diseño propio alineado a referentes de gobierno digital (gob.pe, USWDS, GOV.UK). |
| 2 | Arquitectura y tecnologías | 🟢 Cumple | Stack open-source, maduro, 12-factor; compatible con estándares de la SGTD. |
| 3 | Interoperabilidad | 🟡 Preparado | Arquitectura lista para exponer API REST; sin integración activa a sistemas externos. |
| 4 | Accesibilidad | 🟢 Cumple | Diseñado a nivel **WCAG 2.1 AA** (NTP-ISO/IEC 40500). |
| 5 | Idiomas | 🟡 Preparado | Español pleno; infraestructura i18n de Django lista para lenguas originarias (Ley 29735). |
| 6 | Aplicación móvil | 🟢 Cumple | Web responsive mobile-first **instalable como PWA** (manifest + service worker). |
| 7 | Seguridad y datos personales | 🟢 Cumple | Implementa principios de la **Ley 29733**; buenas prácticas de seguridad en producción. |

Leyenda: 🟢 cumple / implementado · 🟡 parcial o preparado para crecer · 🔴 no aplica / no implementado.

---

## 1. Identidad visual y diseño

**Lineamiento oficial aplicable**
- Guía y manual de la **Plataforma Digital Única del Estado (gob.pe)** para servicios digitales.
- Manuales de identidad institucional propios de cada entidad.

**Qué cumple el prototipo**
- Sistema de diseño documentado en `branding.md`: paleta institucional, tipografía única
  (Inter), grilla de 8 px, sistema de iconos (Lucide).
- Criterios tomados de referentes de **gobierno digital**: gob.pe, U.S. Web Design System
  (USWDS) y GOV.UK → paleta sobria, contraste alto, tipografía clara, confianza institucional.
- Identidad consistente y aplicada en toda la interfaz (header, footer, dashboards, landing).

**Evidencia en el código**
- `branding.md` — especificación completa del sistema de diseño.
- `templates/base.html` (config de Tailwind, tokens de color, tipografía).
- `static/img/` — escudo UNSA oficial con texto alternativo.

**Trabajo futuro**
- Si el sistema se transfiere a una entidad del Estado, sustituir la identidad UNSA por la
  identidad institucional correspondiente y validar contra su manual de marca.

---

## 2. Arquitectura de software y tecnologías aprobadas

**Lineamiento oficial aplicable**
- **D.L. 1412** — Ley de Gobierno Digital, y normas de la **Secretaría de Gobierno y
  Transformación Digital (SGTD, antes SEGD)**.
- No existe un catálogo cerrado de frameworks/lenguajes obligatorios; la exigencia es de
  estándares (seguridad, interoperabilidad, accesibilidad, software público).

**Qué cumple el prototipo**
- Stack **100% open-source y maduro**: Django 6, PostgreSQL, Gunicorn, WhiteNoise.
- Configuración **12-factor**: parámetros y secretos en variables de entorno, no en código.
- Server-rendered (sin dependencias de build de Node), lo que reduce superficie de ataque
  y facilita despliegue y mantenimiento por equipos del Estado.

**Evidencia en el código**
- `requirements.txt` — dependencias del proyecto.
- `conecta_unsa/settings.py` — configuración por variables de entorno.

**Trabajo futuro**
- Validar el stack contra el catálogo/estándares vigentes de la SGTD en el momento del despliegue.

---

## 3. Interoperabilidad

**Lineamiento oficial aplicable**
- **Plataforma de Interoperabilidad del Estado (PIDE)** y el marco de interoperabilidad
  (D.L. 1412 y D.S. 029-2021-PCM).
- Para el dominio forestal: estándares de integración con **SNIFFS (SERFOR)** y **SIGOsfc (OSINFOR)**.

**Qué cumple el prototipo**
- Arquitectura desacoplada (Django) **preparada para exponer una API REST** (p. ej. con
  Django REST Framework) y consumir servicios del PIDE.
- Modelo de datos con campos de procedencia/verificación que permiten distinguir datos
  autodeclarados de datos provenientes de un sistema externo de confianza.

**Estado actual**
- 🟡 El MVP es server-rendered y **no expone aún servicios interoperables** ni integra
  SNIFFS/SIGOsfc. Es una decisión de alcance para el hackathon, no una limitación de diseño.

**Trabajo futuro**
- Exponer API REST documentada (OpenAPI).
- Integración vía PIDE con los sistemas sectoriales que correspondan.

---

## 4. Accesibilidad

**Lineamiento oficial aplicable**
- **NTP-ISO/IEC 40500:2012** (adopción peruana de WCAG 2.0) y, como referencia actual, **WCAG 2.1**.
- Normativa de gobierno digital que exige accesibilidad en plataformas del Estado.
- **Nivel objetivo: AA.**

**Qué cumple el prototipo** — diseñado a nivel **WCAG 2.1 AA**
- **Foco visible** global por teclado (`outline` de alto contraste).
- **Contraste** del color primario 9:1 sobre blanco (supera AA y AAA).
- **Enlace "Saltar al contenido"** (skip link) accesible por teclado.
- **HTML semántico**: `header`, `nav` con `aria-label`, `main`, `footer`.
- **`aria-label`** en controles interactivos (campana de notificaciones, matriz de
  preferencias, botones de acción) e **imágenes con `alt`**.
- **`lang="es"`** declarado en el documento.

**Evidencia en el código**
- `templates/base.html` — foco visible global, skip link, estructura semántica.
- `apps/usuarios/templates/.../perfil.html` — `aria-label` en radios/botones.
- `apps/notificaciones/templates/.../_campana.html` — `aria-haspopup`/`aria-expanded`.
- Commits `cc4f3aa` y `9c70923` — mejoras de a11y y contraste.

**Trabajo futuro / evidencia para el jurado**
- Adjuntar **captura de Lighthouse / axe** con el puntaje de Accesibilidad.

---

## 5. Idiomas

**Lineamiento oficial aplicable**
- **Ley N° 29735** — uso, preservación y desarrollo de las lenguas originarias del Perú.
- Relevante cuando el caso de uso involucra comunidades nativas.

**Qué cumple el prototipo**
- Español pleno, con zona horaria `America/Lima` y moneda `PEN (S/)`.
- Infraestructura de **internacionalización de Django activada** (`USE_I18N = True`,
  `LocaleMiddleware`), lista para añadir traducciones sin refactor.

**Estado actual**
- 🟡 Solo español; aún sin archivos de traducción (`.po/.mo`) ni soporte de lenguas originarias.

**Evidencia en el código**
- `conecta_unsa/settings.py` — `LANGUAGE_CODE`, `USE_I18N`, `LocaleMiddleware`.

**Trabajo futuro**
- Marcar textos con `{% trans %}` y publicar al menos un lema/elementos clave en quechua
  como demostración de cumplimiento de la Ley 29735.

---

## 6. Aplicación móvil

**Lineamiento oficial aplicable**
- Lineamientos de servicios digitales del Estado (mobile-first, accesibilidad).
- No hay obligación general de publicar en tiendas; se prioriza el acceso web universal.

**Qué cumple el prototipo**
- **Diseño responsive mobile-first** (Tailwind), con navegación adaptada a móvil.
- **PWA instalable**: `manifest.webmanifest` (nombre, íconos 192/512 + maskable, tema
  institucional, `display: standalone`) y *service worker* con respaldo offline básico.
  Se instala desde el navegador del celular como una app, **sin pasar por tiendas**.

**Evidencia en el código**
- `templates/pwa/manifest.webmanifest` y `templates/pwa/sw.js`.
- `conecta_unsa/urls.py` — rutas `/manifest.webmanifest` y `/sw.js` (service worker
  servido desde la raíz para alcanzar todo el sitio).
- `templates/base.html` — enlace al manifest, `theme-color` y registro del service worker.
- `static/img/pwa/` — íconos de la app (192, 512 y 512 *maskable*).

**Nota técnica**
- La instalación PWA requiere HTTPS (o `localhost`). En producción el sitio fuerza HTTPS,
  por lo que la app es instalable; en desarrollo funciona vía `localhost`.

**Trabajo futuro**
- Estrategia de caché offline más rica y notificaciones push si el caso lo requiere.

---

## 7. Seguridad y datos personales

**Lineamiento oficial aplicable**
- **Ley N° 29733** — Protección de Datos Personales, y su reglamento **D.S. 003-2013-JUS**
  (Autoridad Nacional de Protección de Datos Personales — MINJUS).
- **NTP-ISO/IEC 27001** — gestión de seguridad de la información (adopción progresiva en
  entidades públicas).

**Qué cumple el prototipo**

*Datos personales (Ley 29733):*
- Páginas de **privacidad y términos** que citan expresamente la Ley 29733.
- **Consentimiento informado** registrado (campo y marca temporal).
- **Control del titular**: acceso, rectificación, eliminación y revocación.
- Datos sensibles **opt-in y no indexables** (credencial pública solo por enlace).

*Seguridad de la información:*
- En producción: **HTTPS forzado**, HSTS (con preload), `SECURE_CONTENT_TYPE_NOSNIFF`.
- **Cookies seguras** de sesión y CSRF; protección CSRF activa.
- **Secretos en variables de entorno** (nunca en el repositorio).
- **Control de acceso por rol** y administración por *allowlist* (sin autoasignación de rol).

**Evidencia en el código**
- `conecta_unsa/settings.py` — endurecimiento con `DEBUG=False`, cookies seguras, HSTS.
- `apps/usuarios/models.py` — consentimiento y control de visibilidad de datos.
- `apps/core/templates/.../privacidad.html` y `terminos.html` — base legal citada.
- `apps/usuarios/decorators.py` y `adapters.py` — control de acceso y allowlist.

**Trabajo futuro**
- Registro del banco de datos personales ante la ANPD.
- Hacia un SGSI conforme a NTP-ISO/IEC 27001 (proceso organizacional, no solo técnico).

---

## Marco normativo de referencia

| Tema | Norma / referencia |
|------|--------------------|
| Gobierno digital | D.L. 1412 — Ley de Gobierno Digital; D.S. 029-2021-PCM |
| Accesibilidad | NTP-ISO/IEC 40500:2012 (WCAG 2.0); WCAG 2.1 (referencia AA) |
| Datos personales | Ley N° 29733; D.S. 003-2013-JUS |
| Seguridad de la información | NTP-ISO/IEC 27001 |
| Interoperabilidad | Plataforma de Interoperabilidad del Estado (PIDE) |
| Lenguas originarias | Ley N° 29735 |
| Identidad / servicios digitales | Guía de la Plataforma Digital Única del Estado (gob.pe) |

> **Nota.** Las referencias normativas se citan por su denominación oficial; se recomienda
> verificar la versión vigente y la URL en el portal de la PCM/SGTD y la ANPD al momento
> de la sustentación.
