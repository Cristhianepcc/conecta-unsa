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

| Usuario | Persona | Rol | Acceso en la demo | Destino |
|---|---|---|---|---|
| `demo_egresado` | María Fernanda Quispe Mamani | Estudiante / Egresado | Login → "Soy de la UNSA" → botón **Egresado** | Dashboard del egresado (feed) |
| `demo_admin` | Lucía Herrera Paredes | Administrativo | Login → "Soy de la UNSA" → botón **Administrador** | Panel administrativo (bandeja) |
| `demo_empresa` | Carlos Rivera Núñez | Empresa (reclutador) | Login → "Soy empresa" → `demo_empresa` / `demo12345` | Dashboard de empresa |

### Perfil de `demo_egresado` (para lucir el matching)
- **Carrera:** Ingeniería Industrial · **Estado:** Egresado · **Perfil completo**.
- **Preferencias:** tipos preferidos *Trainee / Empleo / Práctica profesional*; frecuencia semanal;
  carrera afín de interés: *Administración*.
- **Credenciales:**
  - 🟢 Inglés B2 — Centro de Idiomas UNSA *(verificado)*
  - 🟢 Tesis: Optimización de la línea de producción (2025) *(verificado)*
  - 🟢 Prácticas en planta — sector industrial *(verificado)*
  - ⚪ Delegada de Ingeniería Industrial (2023) *(autodeclarado)*
  - ⚪ Voluntariado TECHO (2024) *(autodeclarado)*

### Perfil de `demo_admin`
- En la **AdminAllowlist** (`demo.admin@unsa.edu.pe`) → el sistema lo reconoce como administrativo.

### Perfil de `demo_empresa`
- Empresa **verificada**: *Soluciones Industriales del Sur S.A.C. (SISUR)* — RUC 20100000100,
  CIIU, dirección en el Parque Industrial APIMA, web y descripción.
- Reclutador: Carlos Rivera Núñez · Jefe de RR.HH. · `rrhh@sisur.demo.pe`.

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
