# CONECTA UNSA

> Rediseño del servicio institucional de comunicación y acceso a oportunidades laborales
> para egresados de la Universidad Nacional de San Agustín.
> Hackathon Becas BCP — 3ra Edición · **Equipo 43 - Zenit**.

Pasar de *"enviar todo a todos"* a **comunicación pertinente, organizada y administrable**:
difusión segmentada por carrera, convocatorias transparentes y estandarizadas, y menos carga
operativa para la Bolsa de Trabajo — sin IA, con software público.

---

## 📚 Documentación de planificación

| Documento | Contenido |
|---|---|
| [propuesta.md](propuesta.md) | Problema público, insight, valor, principios de diseño |
| [stack-conecta-unsa.md](stack-conecta-unsa.md) | Stack: Django + PostgreSQL + Alpine/Tailwind + Docker |
| [arquitectura.md](arquitectura.md) | ADR: monolito modular Django, alternativas evaluadas, config-as-data, camino evolutivo |
| [taxonomia-unsa.md](taxonomia-unsa.md) | 3 Áreas → 16 Facultades → 43 Carreras (base de segmentación) |
| [modelo-datos.md](modelo-datos.md) | Convocatoria: 8 tipos, campos legales (Perú), 3 niveles de formulario, transparencia |
| [matching.md](matching.md) | 3 filtros (estado×tipo · carrera · perfil de talento), elegibilidad, demo |
| [flujo-admin.md](flujo-admin.md) | Estados, alertas, duplicados (pg_trgm), semáforo de confianza |
| [auth-roles.md](auth-roles.md) | Estudiante/Egresado (auto-registro) · Administrativo · Empresa (RUC + reclutador) |
| [perfil-preferencias.md](perfil-preferencias.md) | Perfil (2 orígenes), preferencias, credencial verificable opt-in |
| [notificaciones.md](notificaciones.md) | Resumen semanal · envío real con Resend · campana in-app |
| [branding.md](branding.md) | Tokens granate, Inter, logo, sistema visual (gov-digital) |
| [landing-audit.md](landing-audit.md) | Auditoría UI/UX + estructura final de la landing |
| [deploy.md](deploy.md) | Railway (manual, Hobby), Postgres, env vars, dominio grellox.com |
| [proyecto.md](proyecto.md) | Equipo, integrantes, entregables de la hackathon |
| [paginas.md](paginas.md) | Especificación de las 4 pantallas + mockups en `paginas/` |
| [SEED.md](SEED.md) | **Siembra de datos**: `seed_demo`, empresas reales + logos/banners, cuentas y credenciales de demo |
| [A-PRODUCCION.md](A-PRODUCCION.md) | **Checklist para subir a producción** (complementa `deploy.md`): commit de imágenes, env vars, sembrar la BBDD |

---

## 🖥️ Pantallas (mockups en `paginas/`)

1. **Landing institucional** — pública (ver auditoría).
2. **Dashboard del egresado** — convocatorias pertinentes, preferencias, resumen semanal.
3. **Panel administrativo** — bandeja, validación, métricas (template a medida + Django Admin).
4. **Flujo empresa → validación → difusión** — blueprint operativo.

---

## ⚙️ Stack

Django · PostgreSQL · HTML + Alpine.js + Tailwind (CDN) · Resend (correo) ·
Docker Compose (local) · Railway (deploy).

---

## 📐 Especificaciones (Spec-Driven Development)

La implementación se guía por [`specs/`](specs/) — la capa accionable y verificable:

- [`specs/constitucion.md`](specs/constitucion.md) — principios, convención EARS, orden de ejecución, DoD.
- **Transversales:** glosario · modelo-datos canónico · requisitos no funcionales · estrategia de pruebas · seed-demo.
- **13 features** (`00-fundacion` … `12-panel-admin`), cada una con `requirements.md` (qué + EARS), `design.md` (cómo), `tasks.md` (pasos).
- [`specs/_template/`](specs/_template/) — plantilla para nuevas features.
- [`specs/plan-paralelo.md`](specs/plan-paralelo.md) — playbook para construir con **sub-agentes en paralelo** (olas + sync gates).
- [`specs/prompt-implementacion.md`](specs/prompt-implementacion.md) — **prompt maestro** para implementar todo (modo orquestado / secuencial).

Los 15 docs de la raíz son la **capa de decisiones/referencia**; las specs los referencian, no los duplican.

## 🚦 Estado

**Planificación + especificación (SDD) completas.** Siguiente paso: ejecutar `00-fundacion`
(inicializar el proyecto Django) y avanzar feature por feature en orden.
