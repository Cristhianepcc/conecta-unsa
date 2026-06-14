# Matching y Segmentación — CONECTA UNSA

> Cómo el sistema decide **qué convocatorias ve cada persona y en qué orden**.
> Todo por **reglas transparentes y explicables — sin IA** (`propuesta.md` §5/§8).
> Es el "matching inteligente" del reto, pero auditable (mejor que una caja negra para
> un servicio público: genera confianza).

---

## Arquitectura: 3 niveles

```
Gate 1 — ESTADO ACADÉMICO × TIPO   → filtro duro (elegibilidad LEGAL)
Gate 2 — CARRERA                    → filtro duro (segmentación / pertinencia)
Layer 3 — PERFIL DE TALENTO         → ranking blando (credenciales verificadas)
```

- **Gate 1 y 2** deciden *si lo ve* (sí/no).
- **Layer 3** decide *en qué orden lo ve* (afinidad explicable). No oculta nada, solo ordena.

---

## Gate 1 — Estado académico × Tipo (elegibilidad legal)

El estado académico es un dato de **identidad** (idealmente **verificado por el sync
institucional**, no autodeclarado, porque define elegibilidad legal).

**Grado más alto alcanzado** (el posgrado va *encima*, no reemplaza):
> Estudiante → Egresado → Bachiller → Titulado → Magíster → Doctor
> (+ marca opcional: "actualmente cursando posgrado")

Las modalidades formativas son específicas por estado **por ley** (Ley 31572): un estudiante
no puede hacer "práctica profesional"; un titulado no hace "preprofesional".

### Matriz de elegibilidad (configurable por el admin)

| Tipo de convocatoria | Estudiante | Egresado | Titulado | Magíster | Doctor |
|---|:--:|:--:|:--:|:--:|:--:|
| Práctica preprofesional | ✅ | — | — | — | — |
| Práctica profesional | — | ✅ | — | — | — |
| Trainee / Jóvenes Prof. | — | ✅ | ✅ | ✅ | — |
| Empleo / Laboral | — | ✅ | ✅ | ✅ | ✅ |
| Empleo público / CAS | — | ✅ | ✅ | ✅ | ✅ |
| Voluntariado | ✅ | ✅ | ✅ | ✅ | ✅ |
| Beca / Formación | ✅ | ✅ | ✅ | ✅ | ✅ |
| Consultoría / Freelance | opc | ✅ | ✅ | ✅ | ✅ |

> Magíster y Doctor quedan **listos en el modelo** pero **inactivos en la demo** (ver §Demo).
> Agregar un estado = una fila más. Agregar un tipo = una columna más. **Sin reprogramar.**

---

## Gate 2 — Carrera (segmentación)

- La **carrera es la unidad atómica**. Toda convocatoria se guarda como un **conjunto de
  carreras objetivo**.
- Al publicar, se puede dirigir por **Carrera, Facultad o Área**, y el sistema **lo expande**
  a las carreras que contiene (incluso "Área" es un conjunto finito y explícito → nunca es
  "todo a todos").
- El usuario ve la convocatoria si **su carrera ∈ conjunto objetivo**.
- **"O afines"** se modela como `GrupoAfin` configurable (ver `modelo-datos.md` / Brecha B).

---

## Layer 3 — Perfil de talento (ranking explicable)

Dentro de lo que pasó los dos gates, se **ordena por afinidad** usando lo que la universidad
ya sabe del estudiante. Cada dato es una **señal** que una regla pondera (sin IA), y el sistema
**explica** el resultado ("recomendado porque tienes inglés B2 y una tesis publicada").

### Origen del dato (el diferenciador de confianza)
- 🟢 **Verificado institucionalmente** (vino del sync autorizado) → no se puede falsificar.
- ⚪ **Autodeclarado** (lo agregó el egresado) → menor confianza hasta validarse.

### Credenciales (datos que tiene la universidad)
| Credencial | Qué señala | Potencia para |
|---|---|---|
| Centro de Idiomas / lenguas | Idioma verificado | Roles con idiomas |
| Artículos científicos · Tesis | Investigación | Becas, posgrado, I+D |
| Representante estudiantil · Delegación | Liderazgo | Trainee / Jóvenes Prof. |
| Incubadora Jaku | Emprendimiento/innovación | Innovación, startups |
| Intercambios | Adaptabilidad / internacional | Empresas globales |
| Voluntariados · Congresos | Sentido de retribución | (lo que premia el BCP) |
| Prácticas convalidadas | Experiencia previa | Convocatorias con experiencia |
| Olimpiadas (incl. cachimbo) | Excelencia / competitividad | Programas selectivos |
| Becas · Talleres | Mérito / formación continua | Diversos |

### Modelo (una sola tabla flexible)
```
PerfilEgresado
  ├─ estado_academico / grado más alto  (identidad, verificado por sync)
  ├─ carrera (FK)
  └─ Credencial (N)
       ├─ tipo   (idioma, taller, beca, olimpiada, voluntariado, intercambio,
       │          representación, evento, incubadora_jaku, práctica_convalidada,
       │          artículo, tesis)
       ├─ detalle (nombre, nivel, fecha)
       ├─ fuente  (🟢 institucional-verificado | ⚪ autodeclarado)
       └─ visible_para_empresas (bool — control del egresado, Ley 29733)
```

- **Ingesta en producción:** archivo de **sync autorizado** (`propuesta.md` §6.1 — no toca el SIA).
- **En demo:** seed que simula ese sync.
- Más perfil completo → mejor ranking (mismo incentivo de "mejora progresiva" que las empresas → **simetría: empresa transparente ↔ egresado verificado**).

---

## Estrategia de DEMO

| Decisión | Detalle |
|---|---|
| Estados en demo | Solo **pregrado**: Estudiante, Egresado, Titulado |
| Perfiles de muestra | **No se siembran.** Cada quien entra con **su propio Gmail** y completa su perfil; el presentador usa **2–3 cuentas Gmail propias** con estados distintos para mostrar el matching |
| Convocatorias | **Sí se siembran** (15–25) para que haya contenido que mostrar |
| Momento estelar | Una convocatoria que **aparece a uno y se esconde a otro** + el "recomendado porque…" |
| Posgrado (Magíster/Doctor) | En el modelo, **no** en la demo → se menciona como **escalabilidad** |
| Tipos Docencia / Investigación | **Después.** Se mantienen los **8 tipos** |

> En el pitch: *"el modelo ya escala a posgrado, docencia e investigación solo agregando
> configuración, sin tocar código"* → punto de Escalabilidad (20%) sin costo de build.

---

## Grupos "o afines" (GrupoAfin)

- `GrupoAfin` = conjunto **nombrado** de carreras, **editable por el admin sin tocar código**
  (cumple la promesa de "categorías configurables" de `propuesta.md`).
- Ej.: `"Administración o afines"` = { Administración, Economía, Contabilidad, Relaciones Industriales }.
- Una convocatoria puede dirigirse a carreras sueltas **o** a un GrupoAfin (que se expande).
- **Seed inicial:** el sistema siembra un set base razonable (p. ej. "Administración o afines",
  "Ingenierías o afines", "Salud o afines"…) y el admin lo ajusta después.

## Visibilidad del perfil hacia empresas (decisión MVP)

- En el MVP, el perfil de talento se usa **solo internamente** para **ordenar lo que ve el egresado**.
- **No** se expone a las empresas en la demo (evita temas de privacidad y un módulo nuevo de
  "búsqueda de talento" = otro producto).
- El flag `visible_para_empresas` **queda en el modelo**, listo para activarse después
  (con consentimiento del egresado, Ley 29733).

---

## Naming
Alinear el copy a **"estudiantes y egresados"** (no solo "egresados") — coincide con
`propuesta.md` y con el lenguaje del reto BCP ("empleabilidad juvenil").
