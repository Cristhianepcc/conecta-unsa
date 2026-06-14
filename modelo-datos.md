# Modelo de Datos — CONECTA UNSA

> Define la entidad central del sistema: la **Convocatoria**.
> Diseñado bajo dos principios de la propuesta:
> - **Mínima fricción + mejora progresiva de calidad** (empresa publica con lo esencial; completar más da más visibilidad).
> - **Cumplimiento legal peruano** (portal oficial de la universidad → las ofertas deben ser conformes a ley).
>
> ⚠️ Los montos (RMV), topes de jornada y plazos legales NO se hardcodean: viven en la
> tabla **Parámetros Legales** editable por el admin, porque cambian con el tiempo.
> Este documento guía el diseño de campos y validaciones; no es asesoría legal.

---

## 1. Tipos de convocatoria (8)

Aterrizados al contexto peruano (modalidades formativas + mercado laboral + sector público).

| # | Tipo | Para quién | Marco legal de referencia |
|---|------|-----------|---------------------------|
| 1 | **Práctica preprofesional** | Estudiante de pregrado (cursando) | Ley 31572 (Modalidades Formativas) + reglamento |
| 2 | **Práctica profesional** | Egresado reciente | Ley 31572 |
| 3 | **Trainee / Jóvenes Profesionales** | Egresado / bachiller / titulado | D.L. 728 (contrato laboral) |
| 4 | **Empleo / Convocatoria laboral** | Bachiller / titulado | D.L. 728 (LPCL) |
| 5 | **Empleo público / CAS** | Egresados / titulados | D.L. 1057 (en extinción, Ley 31131) / Ley 30057 SERVIR / D.Leg. 276 |
| 6 | **Voluntariado** | Estudiantes y egresados | Ley 28238 (mod. 29094) |
| 7 | **Beca / Formación** | Estudiantes y egresados | Pronabec (Ley 29837) / privadas |
| 8 | **Consultoría / Locación de servicios** | Egresados / titulados | Código Civil art. 1764 (recibo por honorarios, 4ta cat.) |

---

## 2. Campos del formulario (3 niveles)

El formulario es **dinámico** (Alpine.js): muestra/oculta campos según el `tipo`.

### Nivel 1 — Fundamentales (obligatorios para publicar)

Lo mínimo para que la convocatoria funcione. Son **11**:

| Campo | Tipo de dato | Notas |
|---|---|---|
| **Tipo de convocatoria** | enum (8) | Llave: define campos legales y difusión |
| **Título del puesto** | texto | |
| **Empresa / organización** | texto (FK Empresa) | |
| **Carreras / área objetivo** | M2M (taxonomía UNSA) | 🔑 Corazón de la segmentación |
| **Descripción y requisitos** | texto largo | |
| **Modalidad** | enum: Presencial / Remoto / Híbrido | |
| **Ubicación** | texto (ciudad) | |
| **Duración estimada** | texto/estructurado | Cuánto dura la oportunidad (ej. 6 meses, 1 año, Indeterminado, Por proyecto) — distinto de la fecha límite |
| **Fecha límite de postulación** | fecha | Caduca la oferta |
| **Cómo postular** | URL o email | Sin esto la oferta es inútil |
| **Email de contacto** | email | Anti-spam + trazabilidad |
| ☑ **Declaración de no discriminación** | bool (oblig.) | Ley 26772 — 1 clic |

### Nivel 2 — Obligatorios por ley, según el tipo (condicionales)

Solo se muestran/exigen cuando el `tipo` los activa:

| Campo dependiente | 1·Preprof | 2·Profes | 3·Trainee | 4·Empleo | 5·CAS | 6·Voluntar. | 7·Beca | 8·Consult. |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Requiere **convenio UNSA** | ✅ oblig | ✅ | — | — | — | — | — | — |
| **Ciclo/semestre mínimo** | ✅ | — | — | — | — | opc | opc | — |
| **Tiempo máx. de egreso** | — | ✅ | opc | — | — | — | — | — |
| **Subvención / Remuneración / Honorario** *(nombre y validación según tipo)* | subvención ≥ mín | subvención ≥ mín | sueldo ≥ RMV | sueldo ≥ RMV | honorario | ❌ bloqueado | monto beca | honorario |
| **Jornada (h/sem)** con tope legal | ≤ 30h | ≤ 48h | full/part | full/part | full/part | libre | — | — |
| **Incluye EsSalud / seguro** | ✅ | ✅ | benef. ley | benef. ley | — | recomend. | — | — |
| **Régimen laboral** (728/CAS/276/SERVIR/locación) | — | — | 728 | 728 | ✅ | — | — | locación |
| **Bases + cronograma** | — | — | — | — | ✅ | — | opc | — |
| **Entidad otorgante** | — | — | — | — | — | — | ✅ | — |
| Disclaimer **"no genera vínculo laboral"** | — | — | — | — | — | ✅ | ✅ | ✅ |

### Nivel 3 — Opcionales (mejora progresiva → más transparencia y visibilidad)

No bloquean la publicación; suben el % de transparencia y la prioridad de difusión:

- **Banda salarial** (min–max) vs marcar "Confidencial" → mayor impulsor de transparencia
- **N° de vacantes**
- **Logo de la empresa / sector**
- **Beneficios** (capacitación, EPS, movilidad, etc.)
- **Jornada exacta** (full / part-time / horas)
- **Abierta a personas con discapacidad** (Ley 29973)

---

## 3. Normas transversales (aplican a toda convocatoria)

| Norma | Exige | Impacto en el portal |
|---|---|---|
| **Ley 26772 (mod. 27270)** | No discriminación en ofertas | Checkbox obligatorio; no pedir edad/sexo/foto |
| **Ley 29733** | Protección de datos personales | Consentimiento informado del egresado + aviso de privacidad |
| **Ley 29973** | Cuota de empleo discapacidad | Campo "abierta a personas con discapacidad" |
| **Ley 30709** | Igualdad remunerativa M/H | Sustenta el indicador de transparencia salarial |
| **Ley 28983** | Igualdad de oportunidades | Lenguaje inclusivo |

---

## 4. Tabla de Parámetros Legales (configurable por el admin)

Permite que el portal **valide automáticamente** sin tocar código:

| Parámetro | Ejemplo de valor | Uso |
|---|---|---|
| RMV vigente | S/ 1,130 (referencial) | Validar subvención/remuneración mínima |
| Tope jornada práctica preprofesional | 30 h/sem | Validar jornada |
| Tope jornada práctica profesional | 48 h/sem | Validar jornada |
| Plazo máx. de egreso (práct. profesional) | según norma | Validar elegibilidad |

---

## 5. Esquema de entidades (orientación)

```
Area (3) ──< Facultad (16) ──< Carrera (43)
                                   │
Empresa ──< Convocatoria >──── M2M ┘  (carreras objetivo)
                │
                ├─ tipo (enum 8)
                ├─ campos Nivel 1 (comunes)
                ├─ campos Nivel 2 (nullable, según tipo)
                ├─ campos Nivel 3 (nullable, opcionales)
                ├─ estado de validación (pendiente/validada/duplicada/incompleta/rechazada)
                └─ % transparencia (calculado)

ParametroLegal (config admin)
Usuario (egresado / administrativo / empresa)
```

- Una sola tabla `Convocatoria` con todos los campos; los de Nivel 2 y 3 son *nullable*.
- El formulario decide qué mostrar/exigir según `tipo`. Sin tablas extra → fácil de mantener.

### Origen de la convocatoria (admin puede crear)

`propuesta.md` §7: las convocatorias entran por formulario, correo o **carga manual del admin**.
Por eso el admin puede crear convocatorias **incluso de empresas no registradas**:

- **Empresa registrada** = tiene cuenta de reclutador vinculada + estado *activa* → badge **"✓ Verificada"**.
- **Empresa referencial** = la creó el admin con datos básicos, **sin cuenta vinculada** → sin badge.
- No se necesita flag extra: *"¿tiene cuenta de reclutador?"* distingue ambas. El badge se **deriva**.
- El admin crea empresas referenciales y convocatorias **desde Django Admin** (gratis con el panel híbrido).
- Esto hace el portal **útil desde el día 1** y simplifica el **seed** de las 15–25 convocatorias demo.
- Post-MVP: fusionar empresa referencial con su cuenta cuando se registre (no en el MVP).

---

## 6. Reglas de Transparencia

Cada convocatoria recibe un **% de transparencia** calculado como una lista de chequeo
ponderada: cada dato presente suma puntos; el sueldo visible es el de mayor peso.
Sirve para premiar a las empresas claras (más visibilidad) — es la forma numérica del
principio *"mejora progresiva de calidad"* (`propuesta.md` §6.3).

### Pesos (suman 100, configurables por el admin)

| Criterio que suma transparencia | Peso |
|---|---|
| Banda salarial visible (no "Confidencial") | **30** |
| Descripción y requisitos completos | 15 |
| Duración estimada declarada | 10 |
| Modalidad + ubicación especificadas | 10 |
| N° de vacantes declarado | 10 |
| Beneficios detallados | 10 |
| Contacto verificable | 10 |
| Abierta a personas con discapacidad | 5 |

### Umbrales (etiqueta + color)

| Rango | Etiqueta | Color | Efecto |
|---|---|---|---|
| ≥ 80% | Alta transparencia | 🟢 | Prioridad de difusión |
| 50–79% | Media | 🟡 | Difusión normal + sugerencia de completar |
| < 50% | Baja | 🔴 | Se publica con menor visibilidad + aviso al admin |

- **Índice general** (el 86% de la landing) = promedio del % de transparencia de las
  convocatorias activas. Resume la salud del portal en un solo número.

### Sustento del esquema

Se distingue lo respaldado por fuentes de lo que es calibración de diseño:

| Decisión | ¿Sustento? |
|---|---|
| **El sueldo es el factor de mayor peso** | ✅ **Ley 30709** (igualdad remunerativa) y su reglamento **D.S. 002-2018-TR** — política pública peruana de transparencia salarial. ✅ Tendencia regulatoria global: **Directiva UE 2023/970** de transparencia salarial y leyes de EE. UU. (Colorado, Nueva York, California) que **obligan a publicar el rango salarial** en las ofertas. ✅ Observación de la industria: las ofertas con sueldo visible reciben más postulaciones y generan más confianza |
| **"Completar info → más visibilidad"** | ✅ `propuesta.md` §6.3 (mínima fricción + mejora progresiva) |
| **Usar un % de completitud** | ✅ Patrón de UX estándar (medidor tipo "profile strength" de LinkedIn) |
| **Los pesos exactos (30/15/10…) y los cortes (80/50)** | ⚠️ **Calibración de diseño**, no hay norma que fije una fórmula. Por eso son **configurables por el admin sin tocar código** → mantiene la regla "transparente y auditable" (`propuesta.md` §6.4 / §8) y permite afinar con datos reales de uso |

> Conclusión: el **peso alto del sueldo** y el **incentivo por completitud** están respaldados;
> los **números finos son un punto de partida ajustable**, no una verdad absoluta.
