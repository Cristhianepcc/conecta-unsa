# Taxonomía Académica — UNSA

> Estructura jerárquica oficial de carreras de la Universidad Nacional de San Agustín,
> organizada en **3 Áreas → Facultades → Carreras**.
> Base para la categorización de convocatorias en CONECTA UNSA (taxonomías configurables en BD,
> sin IA — ver [stack-conecta-unsa.md](stack-conecta-unsa.md)).

---

## 1. Área de Ingenierías y Ciencias Básicas

Agrupa carreras relacionadas con tecnología, construcción, industria, computación, ciencias exactas y recursos naturales.

### Facultad de Producción y Servicios
- Ingeniería de Sistemas
- Ciencia de la Computación
- Ingeniería Industrial
- Ingeniería Mecánica
- Ingeniería Eléctrica
- Ingeniería Electrónica
- Ingeniería de Telecomunicaciones

### Facultad de Ingeniería Civil
- Ingeniería Civil
- Ingeniería Sanitaria

### Facultad de Ingeniería de Procesos
- Ingeniería Química
- Ingeniería Metalúrgica
- Ingeniería de Materiales
- Ingeniería de Industrias Alimentarias
- Ingeniería Ambiental

### Facultad de Geología, Geofísica y Minas
- Ingeniería Geológica
- Ingeniería Geofísica
- Ingeniería de Minas

### Facultad de Ciencias Naturales y Formales
- Física
- Matemática
- Química

### Facultad de Arquitectura, Urbanismo y Artes
- Arquitectura

---

## 2. Área de Biomédicas

Relacionada con salud, ciencias biológicas, alimentación y producción agropecuaria.

### Facultad de Medicina
- Medicina

### Facultad de Enfermería
- Enfermería

### Facultad de Ciencias Biológicas y Agropecuarias
- Biología
- Agronomía
- Ciencias de la Nutrición
- Ingeniería Pesquera

---

## 3. Área de Ciencias Sociales y Humanidades

Incluye carreras enfocadas en sociedad, administración, derecho, comunicación, educación y cultura.

### Facultad de Administración
- Administración
- Marketing
- Banca y Seguros
- Gestión

### Facultad de Ciencias Contables y Financieras
- Contabilidad
- Finanzas

### Facultad de Economía
- Economía

### Facultad de Derecho
- Derecho

### Facultad de Ciencias Histórico Sociales
- Historia
- Sociología
- Antropología
- Trabajo Social
- Turismo y Hotelería

### Facultad de Educación
- Educación

### Facultad de Filosofía y Humanidades
- Filosofía
- Literatura
- Artes, Música y Plástica

### Facultad de Psicología, Relaciones Industriales y Ciencias de la Comunicación
- Psicología
- Relaciones Industriales
- Ciencias de la Comunicación

---

## Resumen

| Área | Facultades | Carreras |
|---|---|---|
| Ingenierías y Ciencias Básicas | 6 | 19 |
| Biomédicas | 3 | 6 |
| Ciencias Sociales y Humanidades | 7 | 18 |
| **Total** | **16** | **43** |

---

## Notas para el modelo de datos

- Jerarquía: **Área (1) → Facultad (N) → Carrera (N)**.
- Una **Convocatoria** se asocia a una o varias **Carreras** y/o a una **Facultad/Área** completa
  (ej. "Ingeniería de Sistemas o afines" puede mapear a la Facultad de Producción y Servicios o al Área de Ingenierías).
- Las relaciones "o afines" se construyen como agrupaciones configurables sobre esta jerarquía,
  modificables desde el panel administrativo sin tocar código.
