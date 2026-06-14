# Stack Técnico — CONECTA UNSA

> Decisiones alineadas con los principios de diseño público de la propuesta:
> presupuesto limitado, equipo pequeño, software público, sin dependencia de proveedores,
> capacidad reducida de mantenimiento tecnológico.

---

## Frontend

**HTML + Alpine.js + Tailwind CSS (via CDN)**

- Sin build process, sin node_modules, sin compilación
- La interactividad va directo en el HTML con atributos `x-data`, `x-show`, `@click`
- Tailwind se carga con un único `<script>` en el HTML
- Mantenible por cualquier egresado de sistemas sin conocer frameworks complejos
- Django renderiza las vistas con su sistema de templates — frontend y backend en un solo repositorio

---

## Backend

**Django (Python)**

- El Django Admin cubre casi todo el flujo administrativo sin código adicional:
  validación, organización, priorización de convocatorias
- Python es el lenguaje más accesible en entornos académicos peruanos
- Arquitectura monolítica — un solo servidor, un solo equipo, sin microservicios
- Mantenible por practicantes y egresados de la propia UNSA

---

## Base de Datos

**PostgreSQL**

- Las relaciones carrera ↔ categoría ↔ convocatoria son naturalmente relacionales
- Soporta búsqueda de texto para filtrado básico de convocatorias
- Open source, auditable, sin licencias

---

## Categorización

**Taxonomías configurables en base de datos**

- Sin IA, sin modelos de lenguaje
- Reglas transparentes y auditables definidas por el administrador
- Ejemplo:

```
"Administración o afines"
  → Administración
  → Economía
  → Contabilidad
  → Relaciones Industriales
```

- Modificables sin tocar código — solo desde el panel administrativo

---

## Notificaciones

**Cron job + SMTP institucional**

- Una tarea programada (cron) agrupa convocatorias del período y envía un único resumen consolidado
- Sin Celery, sin Redis — innecesarios para el volumen de una universidad
- Usa el servidor SMTP institucional existente — sin dependencia de servicios externos (SendGrid, Mailgun, etc.)
- Respeta el principio: "más mensajes no significa mejor comunicación"

---

## Infraestructura

**Docker Compose en servidor propio de la UNSA**

- Un solo archivo `docker-compose.yml` levanta todo el sistema:
  Django + PostgreSQL + Nginx
- Replicable a otras universidades modificando solo taxonomías y configuración
- Sin dependencia de proveedores cloud (Railway, Vercel, AWS, etc.)
- Despliegue documentado y transferible entre equipos

```
┌─────────────────────────────────┐
│         Servidor UNSA           │
│                                 │
│  ┌─────────┐   ┌─────────────┐  │
│  │  Nginx  │──▶│   Django    │  │
│  └─────────┘   └──────┬──────┘  │
│                       │         │
│               ┌───────▼──────┐  │
│               │  PostgreSQL  │  │
│               └──────────────┘  │
│                                 │
│  Cron → resúmenes consolidados  │
│  SMTP institucional → correos   │
└─────────────────────────────────┘
```

---

## Resumen de Decisiones

| Principio de la propuesta | Decisión técnica |
|---|---|
| Presupuesto limitado | Todo open source, sin licencias |
| Equipo pequeño | Django Admin cubre el flujo operativo |
| Mantenimiento reducido | Sin frameworks complejos en frontend |
| Independencia de proveedores | Servidor institucional + SMTP propio |
| Replicable a otras universidades | Docker Compose + taxonomías en BD |
| Sin IA compleja | Reglas y categorías configurables |
| Un solo servidor | Monolito Django — sin microservicios |

---

## Lo que se descartó y por qué

| Tecnología | Motivo de descarte |
|---|---|
| Next.js / React | Requiere Node.js adicional, build process, alto mantenimiento |
| Celery + Redis | Complejidad innecesaria para el volumen institucional |
| Railway / Vercel / AWS | Dependencia de proveedores externos, contradice Software Público |
| IA / LLMs | La propuesta lo descarta explícitamente en el MVP |
| Microservicios | Overkill para equipos universitarios pequeños |
| Firebase / Supabase | Dependencia de terceros, sin control institucional |