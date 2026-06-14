"""Constantes canónicas del dominio, centralizadas para evitar duplicación.

Las demás apps importan desde aquí (DRY). Estos valores reflejan
specs/glosario.md y specs/modelo-datos.md (modelo congelado).
"""

# --- Estado académico (glosario) -------------------------------------------
ESTADO_ESTUDIANTE = "estudiante"
ESTADO_EGRESADO = "egresado"
ESTADO_TITULADO = "titulado"

ESTADOS_ACADEMICOS = [
    (ESTADO_ESTUDIANTE, "Estudiante"),
    (ESTADO_EGRESADO, "Egresado"),
    (ESTADO_TITULADO, "Titulado"),
]


# --- Tipos de convocatoria (8) — modelo-datos.md §1 ------------------------
TIPO_PRACTICA_PREPROFESIONAL = "practica_preprofesional"
TIPO_PRACTICA_PROFESIONAL = "practica_profesional"
TIPO_TRAINEE = "trainee"
TIPO_EMPLEO = "empleo"
TIPO_CAS = "cas"
TIPO_VOLUNTARIADO = "voluntariado"
TIPO_BECA = "beca"
TIPO_CONSULTORIA = "consultoria"

TIPOS_CONVOCATORIA = [
    (TIPO_PRACTICA_PREPROFESIONAL, "Práctica preprofesional"),
    (TIPO_PRACTICA_PROFESIONAL, "Práctica profesional"),
    (TIPO_TRAINEE, "Trainee / Jóvenes Profesionales"),
    (TIPO_EMPLEO, "Empleo / Convocatoria laboral"),
    (TIPO_CAS, "Empleo público / CAS"),
    (TIPO_VOLUNTARIADO, "Voluntariado"),
    (TIPO_BECA, "Beca / Formación"),
    (TIPO_CONSULTORIA, "Consultoría / Locación de servicios"),
]


# --- Criterios de transparencia (suman 100) — modelo-datos.md §6 -----------
CRITERIOS_TRANSPARENCIA = [
    ("banda_salarial", "Banda salarial visible (no «Confidencial»)", 30),
    ("descripcion_completa", "Descripción y requisitos completos", 15),
    ("duracion", "Duración estimada declarada", 10),
    ("modalidad_ubicacion", "Modalidad + ubicación especificadas", 10),
    ("vacantes", "N.º de vacantes declarado", 10),
    ("beneficios", "Beneficios detallados", 10),
    ("contacto", "Contacto verificable", 10),
    ("discapacidad", "Abierta a personas con discapacidad", 5),
]


# --- Matriz de elegibilidad estado × tipo (matching.md, demo pregrado) -----
# Para cada estado académico, el conjunto de tipos de convocatoria permitidos.
MATRIZ_ELEGIBILIDAD = {
    ESTADO_ESTUDIANTE: {
        TIPO_PRACTICA_PREPROFESIONAL,
        TIPO_VOLUNTARIADO,
        TIPO_BECA,
        TIPO_CONSULTORIA,  # opcional para estudiante
    },
    ESTADO_EGRESADO: {
        TIPO_PRACTICA_PROFESIONAL,
        TIPO_TRAINEE,
        TIPO_EMPLEO,
        TIPO_CAS,
        TIPO_VOLUNTARIADO,
        TIPO_BECA,
        TIPO_CONSULTORIA,
    },
    ESTADO_TITULADO: {
        TIPO_TRAINEE,
        TIPO_EMPLEO,
        TIPO_CAS,
        TIPO_VOLUNTARIADO,
        TIPO_BECA,
        TIPO_CONSULTORIA,
    },
}


# --- Parámetros legales base (seed) — modelo-datos.md §4 -------------------
PARAMETROS_LEGALES_BASE = [
    ("rmv", "1130", "Remuneración Mínima Vital vigente (S/), referencial."),
    ("tope_jornada_practica_preprofesional", "30", "Tope de jornada (h/sem) práctica preprofesional."),
    ("tope_jornada_practica_profesional", "48", "Tope de jornada (h/sem) práctica profesional."),
    ("plazo_max_egreso_meses", "12", "Plazo máx. de egreso para práctica profesional (meses)."),
    ("umbral_similitud_duplicado", "0.6", "Umbral pg_trgm (0-1) para marcar posible duplicado."),
    ("limite_difusion_30d", "5", "Máx. de convocatorias por empresa en 30 días antes de alertar exceso."),
]
