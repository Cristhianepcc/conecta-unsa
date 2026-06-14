# Prompt Maestro de Implementación — CONECTA UNSA

> Copia el bloque de abajo y dáselo a Claude Code (o al orquestador de agentes) para construir
> **todo** el proyecto siguiendo el SDD. Hay dos modos: **Orquestado** (sub-agentes en paralelo)
> y **Secuencial** (un solo agente). Usa el que prefieras.

---

## MODO A — Orquestado (sub-agentes en paralelo)

```
Eres el INGENIERO LÍDER que va a construir CONECTA UNSA completo, orquestando sub-agentes en paralelo.

## Fuente de verdad (léela antes de empezar)
- specs/constitucion.md         → principios, convención EARS, orden, Definition of Done
- specs/plan-paralelo.md        → olas, sync gates, tabla de agentes, reglas anti-conflictos
- specs/modelo-datos.md         → esquema canónico (CONGELADO, no se modifica)
- specs/glosario.md             → lenguaje ubicuo
- specs/requisitos-no-funcionales.md, specs/estrategia-pruebas.md, specs/seed-demo.md
- Cada feature: specs/NN-nombre/{requirements,design,tasks}.md

## Objetivo
Implementar las 13 features (00→12) hasta que TODOS sus criterios EARS tengan tests en verde.
Stack y reglas: las de specs/constitucion.md (Django 3.13, PostgreSQL, Alpine/Tailwind, sin IA,
config-as-data, allauth Google + auth empresa, Resend, deploy Railway). NO te desvíes de las specs.

## Cómo ejecutar (por OLAS, ver specs/plan-paralelo.md §3)
1. OLA 0 — Construye tú mismo `00-fundacion` (secuencial). Deja listos los puntos de integración:
   settings.py con TODAS las apps en INSTALLED_APPS, urls.py raíz con include() de cada app,
   requirements.txt, .python-version (3.13), Procfile/railway.json, docker-compose.yml, .env.example,
   y los modelos config-as-data en `core` (ParametroLegal, PesoTransparencia, ReglaElegibilidad, AdminAllowlist).
   Corre migraciones + tests. Esto desbloquea el paralelismo.

2. OLAS 1–6 — Para cada ola, LANZA EN PARALELO un sub-agente por feature (un Agent por spec,
   aislado en git worktree). Dale a cada uno el "Prompt por sub-agente" de abajo, sustituyendo
   <NN-nombre> y <apps>. Las features de la MISMA ola corren a la vez; las olas son secuenciales.

   Ola 1: 01-taxonomia ║ 02-autenticacion
   Ola 2: 03-empresas ║ 07-perfil-credencial
   Ola 3: 04-convocatorias
   Ola 4: 05-matching ║ 06-flujo-admin
   Ola 5: 08-notificaciones ║ 09-landing
   Ola 6: 10-dashboard-estudiante ║ 11-dashboard-empresa ║ 12-panel-admin

3. SYNC GATE entre olas (specs/plan-paralelo.md §7): mergea las ramas terminadas a main,
   corre makemigrations+migrate y la suite de tests completa, verifica seed_demo, y recién
   entonces abre la siguiente ola desde main actualizado. NO abras una ola si la anterior no está verde.

## Reglas invariables
- El modelo canónico (specs/modelo-datos.md) está CONGELADO. Si un agente necesita cambiarlo,
  que se DETENGA y lo reporte; tú decides en el sync gate.
- Cada sub-agente edita SOLO los archivos de su(s) app(s). Nadie toca settings.py/urls.py raíz
  tras la Ola 0 (salvo agregar una dependencia a requirements.txt, que es aditivo).
- Definition of Done por feature = tasks.md completo + tests de sus criterios EARS en verde.
- Sin secretos en el repo (van por variables de entorno).

## Cierre del proyecto
- Corre la suite COMPLETA de tests (todo verde).
- Corre `python manage.py seed_demo` y verifica que landing/dashboards muestran datos reales.
- Smoke test: levantar, entrar por las 2 puertas, publicar una convocatoria, verla difundida.
- Entrega un reporte: features completadas, cobertura de criterios EARS, pendientes (escudo UNSA,
  claves OAuth/Resend que el usuario debe configurar), y la lista de variables de entorno para Railway.

## Prompt por sub-agente (úsalo al lanzar cada Agent)
---
Eres el sub-agente de la feature <NN-nombre> de CONECTA UNSA. Trabajas en la rama feat/<NN-nombre>.
Contrato (léelos y obedécelos): specs/constitucion.md, specs/modelo-datos.md, specs/glosario.md
(NO modifiques los dos últimos) y specs/<NN-nombre>/{requirements,design,tasks}.md.
Reglas: edita SOLO los archivos de la(s) app(s) <apps>; NO toques settings.py, urls.py raíz ni otras
apps (ya los dejó 00-fundacion); implementa tasks.md EN ORDEN; escribe un test por cada criterio EARS;
corre migraciones y tests hasta que pasen. Si necesitas cambiar el modelo canónico, NO lo hagas:
reporta y detente. Entregable: tasks.md marcado + resumen de lo creado + estado de tests + bloqueos.
---
```

---

## MODO B — Secuencial (un solo agente, sin paralelizar)

```
Eres un INGENIERO que va a construir CONECTA UNSA completo, feature por feature.

Fuente de verdad: specs/constitucion.md, specs/modelo-datos.md, specs/glosario.md,
specs/requisitos-no-funcionales.md, specs/estrategia-pruebas.md, specs/seed-demo.md,
y specs/NN-nombre/{requirements,design,tasks}.md de cada feature.

Construye EN ESTE ORDEN (respeta dependencias):
00-fundacion → 01-taxonomia → 02-autenticacion → 03-empresas → 04-convocatorias →
05-matching → 06-flujo-admin → 07-perfil-credencial → 08-notificaciones →
09-landing → 10-dashboard-estudiante → 11-dashboard-empresa → 12-panel-admin

Por cada feature:
1) Lee sus 3 specs. 2) Implementa tasks.md en orden. 3) Escribe un test por cada criterio EARS.
4) Corre migraciones + tests hasta verde. 5) Marca tasks.md y pasa a la siguiente.

Reglas: obedece la constitución; NO modifiques el modelo canónico; sin secretos en el repo;
Definition of Done = tests EARS en verde.

Al terminar: suite completa en verde + `seed_demo` + smoke test + reporte de pendientes
(escudo UNSA, claves OAuth/Resend) y variables de entorno para Railway.
```

---

## Notas de uso
- **Modo A** es más rápido (paralelo) pero requiere un orquestador que pueda lanzar sub-agentes
  con aislamiento por worktree. **Modo B** es más simple y predecible.
- En ambos, el agente **no improvisa**: las specs son el contrato. Si algo falta en una spec,
  se detiene y lo reporta (no inventa).
- Pendientes que el usuario debe aportar fuera del código: **escudo UNSA oficial**, **GOOGLE_CLIENT_ID/SECRET**,
  **RESEND_API_KEY + dominio remitente**, y los **nombres de los 4 integrantes** (para el PDF).
