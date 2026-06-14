# Arquitectura — CONECTA UNSA

> Registro de decisión arquitectónica (ADR). Incluye la arquitectura elegida, las alternativas
> evaluadas y el camino evolutivo. Amarra a los principios de `propuesta.md` y `stack-conecta-unsa.md`:
> software público, equipo pequeño, sin IA, auditable, replicable, sin proveedores externos.

---

## 0. ¿Qué "escalabilidad" importa aquí?

Una bolsa de trabajo universitaria **no** necesita aguantar millones de usuarios concurrentes
(escala universitaria = decenas de miles, tráfico modesto). La escalabilidad que importa es:

| Eje | ¿Relevante? |
|---|---|
| **De alcance/configuración** (más carreras, reglas, posgrado) | 🔴 Crítico |
| **De replicación** (otras universidades lo adoptan) | 🔴 Crítico |
| **Organizacional** (equipo pequeño lo mantiene) | 🔴 Crítico |
| De tráfico (millones de requests) | 🟢 Secundario |

Elegir optimizando el eje equivocado (tráfico) pierde en los ejes que sí importan.

---

## 1. Decisión: Monolito modular Django, renderizado en el servidor

Un solo proyecto Django dividido en **apps-módulo**. **No** microservicios, **no** SPA separada.

**Por qué:** equipo pequeño (un repo, un deploy, un lenguaje), sin build de Node (templates +
Tailwind/Alpine por CDN), todo open source sin proveedores atados.

---

## 2. Alternativas evaluadas

| Arquitectura | Software público / control | Mantenible (equipo chico) | Django Admin gratis | Escala alcance/config | Replicable | Build MVP |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **1. Monolito modular Django (SSR)** | ✅ | ✅ | ✅ | ✅✅ | ✅ | ✅ |
| 2. Django API (DRF) + SPA React | ✅ | ⚠️ 2 stacks | ✅ | ✅ | ⚠️ | ⚠️ lento |
| 3. Next.js full-stack | ⚠️ Node | ⚠️ | ❌ lo construyes | ✅ | ⚠️ | ✅ |
| 4. Supabase/Firebase (BaaS) | ❌ datos fuera | ✅ | ❌ | ✅ tráfico | ❌ lock-in | ✅ |
| 5. Microservicios | ✅ | ❌❌ | ❌ | ⚠️ tráfico | ❌ complejo | ❌ |

**Por qué cae cada una:**
- **2 (API + SPA):** dos bases de código + build de Node hoy; la API es útil a futuro, no ahora
  (el monolito puede exponerla después).
- **3 (Next.js):** lo descarta `stack-conecta-unsa.md`; **pierdes Django Admin** (construirías todo
  el CRUD); Python es más accesible para mantenimiento en contexto académico peruano.
- **4 (BaaS):** descartado por el stack doc; **datos sensibles del estudiante (Ley 29733) saldrían
  del control institucional** → una universidad pública necesita soberanía de datos; lock-in mata replicación.
- **5 (Microservicios):** la propuesta dice "monolito, sin microservicios"; complejidad operativa
  sin beneficio a escala universitaria.

**Veredicto:** la Opción 1 domina los ejes de escalabilidad que importan (alcance, replicación,
equipo) **respetando todos los principios**. La escala de alcance no la da la infraestructura,
la da el diseño **"configuración-como-datos"** (§5).

---

## 3. Capas

```
Templates (Django) + Tailwind + Alpine.js   ← Presentación (server-rendered)
Vistas (controllers delgados)               ← orquestan, sin lógica de negocio
CAPA DE SERVICIOS                            ← matching, transparencia, duplicados
Modelos (Django ORM)                         ← datos + reglas simples
PostgreSQL (+ pg_trgm)                        ← persistencia
```

---

## 4. Apps (módulos)

| App | Responsabilidad |
|---|---|
| `taxonomia` | Área · Facultad · Carrera · GrupoAfin |
| `usuarios` | Usuario+rol · Egresado (estado, credenciales) · AdminAllowlist · preferencias |
| `empresas` | Empresa (RUC, referencial) · Reclutador · estados |
| `convocatorias` | Convocatoria (8 tipos) · estados · alertas · transparencia · carreras objetivo |
| `matching` | Motor (servicios): elegibilidad · filtro por carrera · ranking explicable |
| `notificaciones` | Resumen semanal (cron) · Resend · campana in-app |
| `core` | Settings · parámetros configurables · base templates · utilidades |

Apps separadas = módulos reutilizables e independientes (otra universidad cambia `taxonomia` y poco más).

---

## 5. Decisión central: "Configuración-como-datos"

Todo lo que podría cambiar vive en **tablas editables por el admin**, no hardcodeado:
taxonomía/GrupoAfin · matriz de elegibilidad (estado×tipo) · pesos de transparencia ·
parámetros legales (RMV, jornadas) · allowlist de admins.

**Por qué es la decisión más importante:**
- **Auditable** → cada regla es un dato visible (la propuesta exige "reglas transparentes y auditables").
- **Escalable sin programar** → posgrado = una fila; cambiar RMV = editar un valor. Es el argumento
  de Escalabilidad (20% de la rúbrica): *"crece con configuración, no con código"*.
- **Mantenible** → el admin ajusta reglas sin un programador.

---

## 6. Capa de servicios (lógica fuera de vistas/modelos)

Matching, cálculo de transparencia y detección de duplicados en módulos de servicio dedicados.

- **Sin IA, explicable:** cada regla es una función legible y testeable. El matching = filtros
  (querysets del ORM: elegibilidad + carrera) + ranking (función de puntaje que **devuelve el motivo**).
- **Testeable:** la lógica crítica se prueba aislada (lo único que vale cubrir con tests en el MVP).

---

## 7. Otras decisiones

| Tema | Decisión | Por qué |
|---|---|---|
| Auth | `django-allauth` (Google) + Django auth (empresa) | Estándar probado; no reinventar seguridad |
| Admin | Django Admin (híbrido) + templates a medida | Operación sin construir CRUD |
| Notificaciones | Comando `manage.py` + cron Railway + Resend | "Sin Celery/Redis" (propuesta); simple |
| Config | 12-factor, env vars, settings por entorno | Deploy reproducible, secretos fuera del repo |
| Runtime | Python 3.13 · Gunicorn · WhiteNoise · `dj-database-url` | Estable, estándar Railway |

---

## 8. Camino evolutivo (no nos encierra)

```
HOY:  Monolito modular (un deploy, simple)
  ├─ ¿app móvil?       → expones API REST desde el mismo Django (DRF)
  ├─ ¿módulo crece?    → lo extraes (ya está aislado por app)
  └─ ¿más tráfico?     → más workers Gunicorn + caché + réplica de lectura Postgres
```

Patrón **"monolito primero, extraes después"** (Fowler): empiezas simple y la estructura modular
deja crecer sin reescribir. Las otras opciones cobran la complejidad **hoy** por una escala que
quizás nunca llegue.

---

## Conclusión

Un sistema **simple de operar** (monolito, sin piezas exóticas) pero **inteligente por configuración**
(reglas como datos auditables) — exactamente lo que necesita una universidad pública: poco
mantenimiento, máximo control, replicable.
