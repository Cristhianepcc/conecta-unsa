# 🚀 EMPEZAR AQUÍ — CONECTA UNSA

> Nota de arranque para implementar el proyecto en un chat nuevo (sin contexto previo).
> **Todo** está documentado: planificación en los `.md` de la raíz, especificación en `specs/`.

---

## 1. Mensaje para arrancar la implementación (copia y pega en el chat nuevo)

```
Proyecto: CONECTA UNSA (en este directorio).
Toda la planificación y especificación ya está hecha en specs/ y en los .md de la raíz.

Lee specs/prompt-implementacion.md y ejecuta el MODO B (secuencial) para construir
TODO el proyecto siguiendo las specs. Empieza por la feature 00-fundacion y avanza
en orden hasta 12-panel-admin. Respeta la constitución y el modelo de datos canónico
(no los modifiques). Definition of Done = tests de criterios EARS en verde.

Antes de escribir código, lee: specs/constitucion.md, specs/modelo-datos.md y
specs/plan-paralelo.md, y dame un plan breve de cómo vas a proceder. Luego arranca.
```

> Para construir en paralelo con sub-agentes, cambia **"MODO B (secuencial)"** por
> **"MODO A (orquestado con sub-agentes en paralelo)"**.

---

## 2. Mapa del proyecto (dónde está todo)

| Carpeta / archivo | Qué es |
|---|---|
| `README.md` | Índice general |
| `SEED.md` | **Siembra de datos** de la demo (`seed_demo`), empresas reales + logos, cuentas y credenciales |
| `A-PRODUCCION.md` | **Checklist para subir a producción** (commit de imágenes, env vars, sembrar la BBDD) |
| `*.md` (raíz) | Capa de **decisiones/referencia** (propuesta, arquitectura, modelo-datos, matching, auth-roles, branding…) |
| `specs/constitucion.md` | Principios, convención EARS, orden de ejecución, Definition of Done |
| `specs/` (transversales) | glosario · modelo-datos canónico · NFR · estrategia-pruebas · seed-demo |
| `specs/NN-nombre/` | 13 features, cada una con `requirements.md` · `design.md` · `tasks.md` |
| `specs/plan-paralelo.md` | Olas, sync gates y reglas para construir en paralelo |
| `specs/prompt-implementacion.md` | **Prompt maestro** (modo A orquestado / modo B secuencial) |
| `paginas/` · `login.png` · `login-empresa-imagenes/` | Mockups de referencia |

---

## 3. Orden de construcción

```
00-fundacion → 01-taxonomia → 02-autenticacion → 03-empresas → 04-convocatorias →
05-matching → 06-flujo-admin → 07-perfil-credencial → 08-notificaciones →
09-landing → 10-dashboard-estudiante → 11-dashboard-empresa → 12-panel-admin
```

---

## 4. Pendientes que debes aportar (no bloquean empezar a construir)

- 🔑 `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` (OAuth Google).
- 🔑 `RESEND_API_KEY` + dominio remitente verificado.
- 🖼️ Escudo UNSA oficial (mientras, placeholder).
- 👥 Nombres de los 4 integrantes — Equipo 43 - Zenit (solo para el PDF de la hackathon).

Las claves se necesitan para **correr/desplegar**, no para construir.

---

## 5. Si el chat nuevo se "pierde"
Recuérdale: **"todo está en `specs/`; el prompt maestro es `specs/prompt-implementacion.md`; el orden está en `specs/constitucion.md`."**
