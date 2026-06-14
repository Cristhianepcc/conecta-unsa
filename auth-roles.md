# Autenticación y Roles — CONECTA UNSA

> Define quién entra al sistema y cómo. 3 roles, **2 puertas de ingreso**.
> Principio de seguridad: **el rol lo decide la identidad, no la pestaña que se elige.**

---

## 1. Roles

| Rol | Qué hace | Cómo entra (autenticación) | Cómo se asigna el rol |
|---|---|---|---|
| **Estudiante / Egresado** | Ve convocatorias pertinentes, configura preferencias y perfil | **Google** (correo institucional `@unsa`) | Automático al entrar |
| **Administrativo** (Bolsa de Trabajo) | Revisa, valida, difunde, ve reportes, activa empresas | **Google** (correo institucional `@unsa`) | **Lista de correos autorizados** (designado por la universidad) |
| **Empresa (Reclutador)** | Registra y gestiona sus convocatorias | **Usuario + contraseña** (+ registro por RUC) | Registro + **activación manual** del admin |

---

## 2. Las 2 puertas de ingreso

En vez de pestañas que "dan" el dashboard, el login tiene **2 puertas** según el método:

| Puerta | Quién | Método |
|---|---|---|
| **"Soy de la UNSA"** (estudiante, egresado o personal) | Comunidad UNSA | **Continuar con Google** |
| **"Soy empresa"** | Empresas externas | Usuario + contraseña |

**El sistema enruta automáticamente después de autenticar** (la pestaña NO otorga permisos):
- Entra con Google → revisa el correo:
  - ¿está en la **lista de admins**? → **dashboard de administrador**.
  - ¿no está? → **dashboard de estudiante/egresado**.
- Entra como empresa → **dashboard de empresa**.

> Mismo botón de Google para estudiante, egresado y admin. El admin no elige nada especial:
> el sistema lo lleva al panel correcto porque **su correo está en la lista autorizada**.
> Así nadie puede "auto-nombrarse" administrador.

---

## 3. Login institucional con Google (comunidad UNSA)

- El correo `@unsa.edu.pe` es **Google (Workspace)** y **no cambia al egresar** → el egresado
  **nunca pierde acceso** (resuelve el problema clásico de las bolsas de trabajo públicas).
- Entrar con Google = **verificación institucional automática** (sin formularios).
- Implementación: **`django-allauth`** + app OAuth de Google (Client ID + Secret como env vars:
  `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`).
- **Primer ingreso** = se crea la cuenta automáticamente y se pide **completar perfil**
  (carrera, estado académico — autodeclarado, porque en demo no hay sync).

### Demo vs Producción
- **Demo:** se acepta **cualquier Gmail** (para que el jurado pruebe en vivo).
- ⚠️ **TODO producción:** restringir a `@unsa.edu.pe` con el parámetro `hd=unsa.edu.pe`
  (un solo cambio) → se convierte en el SSO institucional real.

### Lista de administradores (allowlist)
- La universidad (o el primer superusuario) **agrega manualmente** los correos del personal de
  la Bolsa de Trabajo a la lista de admins. Acción única por administrativo. Nadie se agrega solo.

---

## 4. Flujo de registro de Empresa (estilo UNI)

1. **Login** con usuario / contraseña.
2. Si no tiene cuenta → ingresa su **RUC** → si "Empresa NO registrada" → **Registrar Empresa**.
3. Completa el **formulario** (2 bloques, ver §5).
4. La universidad **verifica y activa** la cuenta manualmente.
5. Empresa activada = **"empresa verificada"** → entra al *semáforo de confianza* (`flujo-admin.md` §4).

**Decisiones del MVP:**
- ✅ Modelo **Empresa (RUC) → Reclutador**, con **activación manual** del admin.
- ✅ **Correo corporativo OPCIONAL** (se permiten dominios gratuitos).
- ✅ **Un (1) reclutador por empresa** (ampliable después).
- Las empresas **no** usan Google (son externas a la UNSA).

---

## 5. Campos del registro de Empresa

### Bloque A — Información de la empresa
RUC ✅ · Tipo de empresa ✅ · CIIU ✅ · Nombre comercial ✅ · Razón social (igual a SUNAT) ✅ ·
Teléfono ✅ · Dirección ✅ · Web · LinkedIn · **Logo (URL)** · **Banner (URL)** · URL de video · Descripción.

> **Logos/banners van como URL** (no subida de archivo) — Railway tiene filesystem efímero
> y los archivos subidos se perderían en cada redeploy (ver `deploy.md`).

### Bloque B — Reclutador asignado (1 por empresa)
DNI ✅ · Nombres ✅ · Apellido paterno ✅ · Apellido materno ✅ · Cargo ✅ ·
Email (corporativo opcional) ✅ · Teléfono / Celular ✅.

---

## 6. Estados de la cuenta Empresa

| Estado | Significado | Quién lo activa |
|---|---|---|
| **Pendiente de activación** | Registro enviado, esperando verificación | Empresa (al registrarse) |
| **Activa** | Verificada → puede publicar convocatorias | Admin |
| **Rechazada** | Datos inválidos / no verificable | Admin |

> La empresa **Pendiente** ve un dashboard limitado (no puede publicar hasta ser activada).

---

## 7. Modelo de datos

```
Usuario (Django User + rol: egresado / admin / reclutador)
  ├─ Egresado   → login Google · carrera (FK) · estado académico · perfil/credenciales
  ├─ Admin      → login Google · en allowlist de correos autorizados
  └─ Reclutador → usuario/contraseña · 1 ── Empresa

Empresa
  ├─ ruc (único) · razón social · nombre comercial · tipo · CIIU
  ├─ teléfono · dirección · web · linkedin · logo_url · banner_url · video_url · descripción
  └─ estado (pendiente / activa / rechazada)

AdminAllowlist → correos institucionales designados como administrativos
```

---

## 8. Datos sembrados para la demo
- **No** se siembran perfiles de estudiante/egresado: cada quien entra con **su propio Gmail**
  y completa su perfil al ingresar.
- **Sí** se siembran **convocatorias** (15–25) y **empresas** de muestra, para que haya
  contenido que mostrar cuando el egresado entra.
- Para demostrar el matching de distintos estados, el presentador puede usar **2–3 cuentas
  Gmail propias**, cada una con un estado distinto (estudiante / egresado / titulado).
