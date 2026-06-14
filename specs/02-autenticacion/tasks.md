# Tareas — 02 Autenticación

## Implementación
- [ ] T1 — Configurar `django-allauth` + provider Google (env: GOOGLE_CLIENT_ID/SECRET).
- [ ] T2 — Modelo Usuario con `rol`; usar AdminAllowlist de core.
- [ ] T3 — Adapter/señal `resolver_rol_y_destino` (allowlist → admin; si no → egresado).
- [ ] T4 — Login empresa (usuario/contraseña) + reset por correo (Resend).
- [ ] T5 — Mixins/decoradores de control por rol (admin_required, empresa_required, egresado_required).
- [ ] T6 — Vista/template `/login` con las 2 puertas (según `login.png`) + consentimiento.
- [ ] T7 — Redirección a `/completar-perfil` en primer ingreso.
- [ ] T8 — Comentar TODO: restringir Google a `@unsa.edu.pe` en producción.

## Pruebas
- [ ] T9 — test CA-3: correo en allowlist → admin; fuera → egresado.
- [ ] T10 — test CA-5: egresado no entra a ruta admin.
- [ ] T11 — test CA-4: empresa entra a su dashboard.

## Cierre
- [ ] DoD cumplido.
