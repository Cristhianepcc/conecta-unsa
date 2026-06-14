# Guía de Demo — CONECTA UNSA

Cómo presentar los 3 flujos (egresado · administrativo · empresa) ante el jurado, sin
configurar Google OAuth. Pensado para un MVP: prioriza mostrar el flujo, no la seguridad.

---

## Enfoque de la demo

- **Objetivo:** que el jurado vea de punta a punta el flujo de cada rol en vivo.
- **Sin fricción de login:** en producción los egresados/administrativos entran con **Google
  institucional** (`@unsa.edu.pe`) y las empresas con usuario/contraseña. Para la demo se
  habilitan **accesos directos** y **usuarios sembrados**, porque montar OAuth en vivo es lento
  y frágil frente a un jurado.
- **Datos vivos pero honestos:** las cifras de la landing/dashboards se **calculan** de datos
  sembrados reales (no hay números inflados); ver `landing-audit.md`.
- **Controlado por un flag:** todo el andamiaje de demo se apaga con `DEMO_MODE=False` y
  desaparece sin tocar código.

---

## Flag `DEMO_MODE`

- Variable de entorno. Por defecto sigue a `DEBUG` (`True` en local).
- **Encendido (`DEMO_MODE=True`):** aparecen los botones de acceso rápido en el login y las
  rutas `/usuarios/demo/<rol>/` funcionan.
- **Apagado (`DEMO_MODE=False`):** los botones desaparecen y esas rutas devuelven **404**.
  → Usar así en **producción real**.
- En el deploy de demo (Railway), poner `DEMO_MODE=True` en las variables de entorno.

---

## Preparar la demo

```bash
python manage.py migrate
python manage.py seed_demo   # taxonomía + config + empresas + convocatorias + usuarios demo
python manage.py runserver
```

`seed_demo` es **idempotente** (se puede correr varias veces).

---

## Usuarios por defecto (sembrados por `seed_demo`)

Contraseña común: **`demo12345`**

| Usuario | Rol | Acceso en la demo | Destino |
|---|---|---|---|
| `demo_egresado` | Estudiante / Egresado | Login → "Soy de la UNSA" → botón **Egresado** | Dashboard del egresado (feed) |
| `demo_admin` | Administrativo | Login → "Soy de la UNSA" → botón **Administrador** | Panel administrativo (bandeja) |
| `demo_empresa` | Empresa (reclutador) | Login → "Soy empresa" → `demo_empresa` / `demo12345` | Dashboard de empresa |

Detalles:
- `demo_egresado` ya tiene **perfil completo** (carrera Ing. de Sistemas, estado egresado) → entra directo al feed con recomendaciones.
- `demo_admin` está en la **AdminAllowlist** → el sistema lo reconoce como administrativo.
- `demo_empresa` tiene una **empresa verificada** (Empresa Demo S.A.C.) → puede publicar convocatorias.

> Empresas de muestra adicionales: `empresa_011` … `empresa_018` (también `demo12345`).

---

## Guion sugerido (≈ flujo)

1. **Landing** (`/`): explicar pertinencia, transparencia (semáforo) y resumen semanal.
2. **Egresado:** login → botón **Egresado** → mostrar el feed filtrado por carrera + el
   "recomendado porque…", guardar una convocatoria, ver el detalle y el botón "Postular".
3. **Empresa:** login → "Soy empresa" (`demo_empresa`/`demo12345`) → publicar una convocatoria
   y mostrar el % de transparencia en vivo; mostrar una "observada" para corregir.
4. **Administrativo:** login → botón **Administrador** → bandeja con alertas (duplicado, baja
   transparencia), aprobar/observar/rechazar; señalar la configuración en Django Admin (`/admin/`).
5. **Cierre:** recalcar "sin IA, reglas auditables, config editable por el admin sin desplegar".

---

## Qué desactivar para producción real

- `DEMO_MODE=False` (oculta botones y bloquea `/usuarios/demo/<rol>/`).
- Configurar `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` (puerta UNSA real).
- Restringir Google a `@unsa.edu.pe` (parámetro `hd`, TODO marcado en `settings.py`).
- Cambiar/eliminar las contraseñas demo y revisar la `AdminAllowlist`.
