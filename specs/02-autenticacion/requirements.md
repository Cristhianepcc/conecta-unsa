# Requisitos — 02 Autenticación

> Obedece [`../constitucion.md`](../constitucion.md). Referencia: [`../../auth-roles.md`](../../auth-roles.md).

## Objetivo
Permitir el ingreso por **2 puertas** (UNSA con Google · Empresa con usuario/contraseña) y enrutar
a cada quien a su dashboard según su **identidad**, no según lo que elija.

## Alcance
- **Incluye:** Google OAuth (allauth), login empresa, allowlist de admins, ruteo de rol, consentimiento, logout, recuperación de contraseña (empresa).
- **No incluye:** registro de empresa (en `03`), perfil del egresado (en `07`).

## Historias de usuario
- **HU-1:** Como egresado/estudiante, quiero entrar con mi correo Google institucional sin crear contraseña.
- **HU-2:** Como administrativo, quiero entrar con el mismo Google y que el sistema me reconozca como admin.
- **HU-3:** Como empresa, quiero entrar con usuario y contraseña.

## Criterios de aceptación (EARS)
- **CA-1:** Cuando un usuario elige "Soy de la UNSA", el sistema debe iniciar el flujo de Google OAuth.
- **CA-2:** Cuando un usuario completa el login con Google por primera vez, el sistema debe crear su cuenta y pedirle completar perfil.
- **CA-3:** Cuando un usuario inicia sesión con Google, si su correo está en `AdminAllowlist`, entonces el sistema debe enrutarlo al **dashboard admin**; si no, al **dashboard de estudiante/egresado**.
- **CA-4:** Cuando una empresa inicia sesión con usuario/contraseña válidos, el sistema debe enrutarla al **dashboard de empresa**.
- **CA-5:** Si un usuario sin rol admin intenta acceder a una ruta admin, entonces el sistema debe denegar (403/redirect).
- **CA-6:** Cuando un usuario se registra, el sistema debe capturar consentimiento de datos (Ley 29733).
- **CA-7 (MVP):** El sistema debe aceptar cualquier Gmail; **TODO producción:** restringir a `@unsa.edu.pe` (`hd=unsa.edu.pe`).

## Dependencias
- `00-fundacion` (allauth instalado, AdminAllowlist en core).

## Notas legales / no funcionales
- NFR-SEC-1/4, NFR-PRIV-1. El rol admin **solo** por allowlist.
