# Plan de Ejecución Paralela con Sub-Agentes — CONECTA UNSA

> Cómo construir el proyecto lanzando **sub-agentes en paralelo**, uno por feature-spec,
> sin que se pisen. Cada sub-agente tiene como **contrato** los 3 archivos de su feature
> (`requirements.md` + `design.md` + `tasks.md`) y obedece [`constitucion.md`](constitucion.md).

---

## 1. Principios

1. **Un sub-agente = una feature-spec.** Su alcance es exactamente su carpeta `NN-xxx/`. No toca otras.
2. **Aislamiento por git worktree.** Cada agente trabaja en su **rama/worktree** propio → cero conflictos de archivos.
3. **El modelo de datos está congelado.** [`modelo-datos.md`](modelo-datos.md) es la verdad compartida.
   Ningún agente lo cambia por su cuenta; si necesita un ajuste, lo **propone** y se acuerda antes (sync gate).
4. **Cada app Django es de un solo dueño.** Un agente solo edita los archivos de **su** app.
5. **Done = tests EARS en verde** (Definition of Done de la constitución).

---

## 2. Regla clave anti-conflictos: los puntos de integración los fija `00`

Los archivos **compartidos** (`settings.py`, `urls.py` raíz, `requirements.txt`) son la causa #1 de
conflictos. Por eso **`00-fundacion` los deja listos de antemano**:

- `INSTALLED_APPS` ya incluye **todas** las apps (aunque estén vacías).
- `urls.py` raíz ya hace `include()` de **cada** `app/urls.py` (aunque estén vacíos).
- `requirements.txt` ya trae las dependencias base.

Así, cada agente de feature **solo edita los archivos de su app** (`models.py`, `services.py`,
`views.py`, `urls.py`, `templates/<app>/`, `tests/`) → no toca los compartidos → **no hay merge hell**.

> Excepción: si una feature necesita una dependencia nueva, la agrega a `requirements.txt`
> (archivo aditivo, conflicto trivial de resolver).

---

## 3. Olas de ejecución (con sync gates)

```
Ola 0:  00-fundacion                              [SECUENCIAL — 1 agente, bloquea a todos]
─────────────────────────── 🔒 sync gate: merge 00 a main ───────────────────────────
Ola 1:  01-taxonomia  ║  02-autenticacion         [2 agentes en paralelo]
─────────────────────────── 🔒 sync gate: merge 01,02 ───────────────────────────────
Ola 2:  03-empresas   ║  07-perfil-credencial     [2 agentes]
─────────────────────────── 🔒 sync gate: merge 03,07 ───────────────────────────────
Ola 3:  04-convocatorias                          [punto de unión — necesita 01+03]
─────────────────────────── 🔒 sync gate: merge 04 ──────────────────────────────────
Ola 4:  05-matching   ║  06-flujo-admin           [2 agentes]
─────────────────────────── 🔒 sync gate: merge 05,06 ───────────────────────────────
Ola 5:  08-notificaciones  ║  09-landing          [2 agentes]
─────────────────────────── 🔒 sync gate ────────────────────────────────────────────
Ola 6:  10-estudiante ║ 11-empresa ║ 12-panel-admin   [3 agentes en paralelo]
```

**Sync gate** = antes de abrir la siguiente ola: mergear las ramas terminadas a `main`,
correr migraciones y tests, y partir las nuevas ramas desde `main` actualizado.

---

## 4. Tabla de lanzamiento de sub-agentes

| Ola | Agente | Spec | Rama / worktree | Depende de | App(s) que edita |
|---|---|---|---|---|---|
| 0 | A0 | `00-fundacion` | `feat/00-fundacion` | — | proyecto + todas (scaffold) |
| 1 | A1 | `01-taxonomia` | `feat/01-taxonomia` | 00 | `taxonomia` |
| 1 | A2 | `02-autenticacion` | `feat/02-auth` | 00 | `usuarios` (auth) |
| 2 | A3 | `03-empresas` | `feat/03-empresas` | 02 | `empresas` |
| 2 | A4 | `07-perfil-credencial` | `feat/07-perfil` | 01,02 | `usuarios` (perfil) |
| 3 | A5 | `04-convocatorias` | `feat/04-convocatorias` | 01,03 | `convocatorias` |
| 4 | A6 | `05-matching` | `feat/05-matching` | 04,07 | `matching` |
| 4 | A7 | `06-flujo-admin` | `feat/06-flujo-admin` | 04,03 | `convocatorias` (flujo) |
| 5 | A8 | `08-notificaciones` | `feat/08-notif` | 05,07 | `notificaciones` |
| 5 | A9 | `09-landing` | `feat/09-landing` | 01,04 | `core` (público) |
| 6 | A10 | `10-dashboard-estudiante` | `feat/10-estudiante` | 05,07,08 | `usuarios`/`convocatorias` (vistas) |
| 6 | A11 | `11-dashboard-empresa` | `feat/11-empresa` | 03,04,06 | `empresas`/`convocatorias` (vistas) |
| 6 | A12 | `12-panel-admin` | `feat/12-admin` | 06,03,04,05 | `core`/`convocatorias` (vistas) |

> Nota de coordinación: en la Ola 4, **A7 (06-flujo)** y en Ola 3 **A5 (04)** tocan la app
> `convocatorias`. Como van en **olas distintas** (04 antes que 06), no chocan. Dentro de una
> misma ola, dos agentes **nunca** comparten app.

---

## 5. Protocolo por sub-agente

Cada agente, en su worktree:
1. **Lee** su `requirements.md` + `design.md` + `tasks.md` + la `constitucion.md` + `modelo-datos.md` + `glosario.md`.
2. **Implementa** las tareas de `tasks.md` en el orden dado.
3. **Escribe los tests** de cada criterio EARS (`estrategia-pruebas.md`).
4. **Corre** migraciones + tests hasta verde.
5. **No** modifica specs ni el modelo canónico (si hace falta, abre nota y espera el sync gate).
6. **Entrega** marcando el `tasks.md` y reportando: qué creó, tests que pasan, dudas/bloqueos.

---

## 6. Prompt plantilla para lanzar un sub-agente

```
Eres el sub-agente de la feature <NN-nombre> de CONECTA UNSA.
Trabajas en el worktree/rama feat/<NN-nombre>.

Contrato (léelos y obedécelos):
- specs/constitucion.md (principios, EARS, DoD)
- specs/modelo-datos.md y specs/glosario.md (NO los modifiques)
- specs/<NN-nombre>/requirements.md, design.md, tasks.md

Reglas:
- Edita SOLO los archivos de la(s) app(s) asignada(s): <apps>.
- NO toques settings.py, urls.py raíz ni otras apps (ya los dejó 00-fundacion).
- Implementa tasks.md en orden. Escribe un test por cada criterio EARS.
- Corre migraciones y tests hasta que pasen.
- Si necesitas cambiar el modelo canónico, NO lo hagas: reporta la necesidad y detente.

Entregable: tasks.md marcado + resumen de lo creado + estado de los tests + bloqueos.
```

---

## 7. Sync gate (checklist entre olas)

- [ ] Mergear ramas terminadas de la ola a `main`.
- [ ] `makemigrations` + `migrate` sin conflictos.
- [ ] Suite de tests completa en verde.
- [ ] `seed_demo` corre ok.
- [ ] Partir las ramas de la siguiente ola desde `main` actualizado.

---

## 8. Cómo se traduce a herramientas

- **Git worktrees:** un worktree por agente (`git worktree add ../ca-<NN> feat/<NN>`), o el
  parámetro de aislamiento de worktree del orquestador de agentes.
- **Paralelismo real:** las features de una misma ola se lanzan **a la vez**; las olas son secuenciales.
- **Equipo humano (4 personas):** mismo mapa, siguiendo los tracks de dueño de
  [README §parallel] (P1 backend-core, P2 egresado, P3 empresa, P4 UI/pública).

---

## Resumen

> El proyecto está **diseñado para paralelizarse**: `00` fija los puntos de integración,
> cada feature vive en su app, el modelo está congelado y cada spec es un contrato verificable.
> Se lanzan sub-agentes por ola (los de una misma ola en paralelo), con un **sync gate** entre olas.
