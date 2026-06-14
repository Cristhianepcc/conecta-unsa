# Glosario — Lenguaje ubicuo

> Términos del dominio que **todas** las specs deben usar igual. Evita que cada feature invente su vocabulario.

| Término | Definición |
|---|---|
| **Área** | Nivel más alto de la taxonomía UNSA (3): Ingenierías y Ciencias Básicas · Biomédicas · Sociales y Humanidades |
| **Facultad** | Subdivisión de un Área (16 en total) |
| **Carrera** | Programa académico (43). **Unidad atómica** del matching |
| **GrupoAfin** | Conjunto nombrado de carreras "o afines", editable por el admin |
| **Estudiante** | Persona cursando pregrado (desde 4º ciclo) |
| **Egresado** | Terminó los cursos; puede ser Bachiller; aún no titulado |
| **Titulado** | Tiene título profesional |
| **Estado académico** | Grado más alto alcanzado: Estudiante / Egresado / Titulado (+ Magíster / Doctor, futuros) |
| **Credencial** | Logro del perfil (idioma, tesis, voluntariado, Jaku…) con **fuente**: verificado o autodeclarado |
| **Perfil de talento** | Conjunto de credenciales + estado + carrera de un egresado |
| **Convocatoria** | Oferta publicada (8 tipos). Entidad central |
| **Tipo de convocatoria** | Práctica preprofesional · profesional · Trainee · Empleo · CAS · Voluntariado · Beca · Consultoría |
| **Empresa registrada** | Tiene cuenta de reclutador activada → badge "Verificada" |
| **Empresa referencial** | Creada por el admin, sin cuenta → sin badge |
| **Reclutador** | Persona de una empresa que gestiona sus convocatorias (1 por empresa en MVP) |
| **Administrativo** | Personal de la Bolsa de Trabajo (rol por allowlist) |
| **Transparencia (%)** | Puntaje ponderado de completitud de una convocatoria (sueldo pesa 30%) |
| **Matriz de elegibilidad** | Tabla configurable estado académico × tipo de convocatoria |
| **Matching** | 3 filtros: elegibilidad (legal) · carrera (segmentación) · ranking (perfil) |
| **Alerta** | Señal del sistema sobre una convocatoria Pendiente (duplicado, incompleta, baja transparencia, exceso) |
| **Semáforo de confianza** | Regla que decide auto-publicar vs revisión humana |
| **Credencial verificable** | Carta de presentación del egresado con URL compartible (opt-in, no social) |
| **Resumen semanal** | Correo consolidado de convocatorias pertinentes (anti-saturación) |
| **Sync institucional** | Carga periódica autorizada de datos UNSA (no toca el SIA). En demo: simulado |
| **Config-as-data** | Reglas en tablas editables por el admin, no en código |
