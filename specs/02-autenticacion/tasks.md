# Tareas — 02 Autenticación

## Implementación
- [x] T1 — Configurar `django-allauth` + provider Google (env: GOOGLE_CLIENT_ID/SECRET).
- [x] T2 — Modelo `Perfil` (1-1 User) con `rol`; usa AdminAllowlist de core.
- [x] T3 — Servicio `resolver_rol_y_destino` (allowlist → admin; reclutador → empresa; resto → egresado).
- [x] T4 — Login empresa (usuario/contraseña) + reset por correo (email backend consola en dev; Resend en 08).
- [x] T5 — Decoradores y mixins de control por rol (admin/empresa/egresado).
- [x] T6 — Vista/template `/login` con las 2 puertas (según `login.png`) + consentimiento.
- [x] T7 — Redirección a `/completar-perfil` en primer ingreso.
- [x] T8 — TODO comentado: restringir Google a `@unsa.edu.pe` (`hd`) en producción.

## Pruebas
- [x] T9 — test CA-3: correo en allowlist → admin; fuera → egresado (+ case-insensitive).
- [x] T10 — test CA-5: egresado no entra a ruta admin/empresa (403); anónimo → login.
- [x] T11 — test CA-4: empresa entra a su dashboard (+ credenciales inválidas).
- [x] CA-1/CA-2/CA-6: login con 2 puertas, primer ingreso y consentimiento (Ley 29733).

## Cierre
- [x] DoD cumplido — 15 tests EARS verdes.

> Notas:
> - El rol lo decide la identidad (allowlist / tipo de login), nunca la pestaña (NFR-SEC-4).
> - Adapters de allauth (`CuentaAdapter`, `AdaptadorSocial`) enrutan post-login.
> - Destinos placeholder creados como puntos de integración: `core:panel_admin` (→ feature 12),
>   `empresas:dashboard` (→ 11), `empresas:registro` (→ 03). Las features dueñas los reemplazan.
> - OAuth de Google: se prueba el ruteo de rol, no el handshake (estrategia-pruebas.md).
