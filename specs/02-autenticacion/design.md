# Diseño — 02 Autenticación

## App
`usuarios` (+ `django-allauth` para Google).

## Modelos
```
Usuario (extiende AbstractUser o perfil 1-1)
  └─ rol : enum(egresado, admin, reclutador)
AdminAllowlist (en core) → email   # define quién es admin
```

## Flujo de ruteo (servicio)
- `resolver_rol_y_destino(user)`:
  - login Google → si `email in AdminAllowlist` → rol=admin → `/admin-panel`;
    si no → rol=egresado → `/dashboard`.
  - login empresa (usuario/contraseña) → rol=reclutador → `/empresa`.
- Se ejecuta en señal `user_logged_in` / adapter de allauth.

## Auth
- **Google:** `django-allauth` con provider Google. `SOCIALACCOUNT_PROVIDERS` con scope email/profile.
  Env: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`.
- **Empresa:** auth nativa Django (username/email + password). Reset por correo (Resend).
- **TODO prod:** parámetro `hd=unsa.edu.pe` en el provider Google.

## Vistas / rutas
| Ruta | Descripción |
|---|---|
| `/login` | Las 2 puertas (Google / empresa) |
| `/accounts/...` | Endpoints allauth |
| `/logout` | Cierre de sesión |
| `/completar-perfil` | Primer ingreso (redirige a `07`) |

## UI
- Login según mockup (`login.png`): pestañas "Soy de la UNSA" (botón Google) / "Soy empresa" (form).
- Copy "estudiantes y egresados". Footer con Política de Privacidad.

## Decisiones
- El rol **no** lo da la pestaña; lo da la identidad (seguridad).
- Admin entra por Google igual que todos; lo distingue la allowlist.

## Trazabilidad
| Criterio | Cubierto por |
|---|---|
| CA-1,2 | allauth + adapter |
| CA-3,4 | `resolver_rol_y_destino` + test |
| CA-5 | mixin/decorador de rol + test |
| CA-6 | checkbox consentimiento + test |
