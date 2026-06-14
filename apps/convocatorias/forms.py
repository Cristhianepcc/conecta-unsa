from django import forms

from .models import Convocatoria


class ConvocatoriaForm(forms.ModelForm):
    """Formulario de convocatoria (reusado por dashboards 11/12).

    El formulario dinámico (mostrar/ocultar Nivel 2/3 según `tipo`) se resuelve en
    la plantilla con Alpine; aquí se define el conjunto completo de campos editables.
    """

    class Meta:
        model = Convocatoria
        # empresa, creada_por y estado los fija la vista; los calculados no se editan.
        exclude = [
            "empresa", "creada_por", "estado", "transparencia_pct",
            "comentario_revision", "fecha_publicacion", "creada_en", "actualizada_en",
        ]
        widgets = {
            "fecha_limite": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Funciones, requisitos y qué ofrece el puesto."}
            ),
            "beneficios": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Ej. EPS, bonos, capacitaciones, horario flexible."}
            ),
            "cronograma": forms.Textarea(attrs={"rows": 3}),
            "titulo": forms.TextInput(attrs={"placeholder": "Ej. Analista de datos junior"}),
            "ubicacion": forms.TextInput(attrs={"placeholder": "Ej. Arequipa (Cercado) / Remoto"}),
            "duracion_estimada": forms.TextInput(
                attrs={"placeholder": "Ej. 6 meses · 1 año · Indefinido"}
            ),
            "vacantes": forms.NumberInput(attrs={"min": 1, "placeholder": "Ej. 3"}),
            "banda_salarial_min": forms.NumberInput(attrs={"min": 0, "step": "50", "placeholder": "S/ desde"}),
            "banda_salarial_max": forms.NumberInput(attrs={"min": 0, "step": "50", "placeholder": "S/ hasta"}),
            "subvencion_remuneracion": forms.NumberInput(attrs={"min": 0, "step": "50", "placeholder": "S/ 0.00"}),
            # Régimen: sugerencias (datalist) pero sigue admitiendo texto libre.
            "regimen": forms.TextInput(
                attrs={"list": "regimenes-list", "placeholder": "Ej. Régimen privado (D.L. 728)"}
            ),
            # Multi-selección clara (varias carreras) en vez del <select multiple>.
            "carreras_objetivo": forms.CheckboxSelectMultiple(
                attrs={"class": "h-4 w-4 accent-granate-700"}
            ),
            "medio_postulacion": forms.TextInput(
                attrs={"placeholder": "https://empresa.pe/empleos  ó  rrhh@empresa.pe"}
            ),
        }
        help_texts = {
            "fecha_limite": "Último día para postular.",
            "duracion_estimada": "Cuánto dura el puesto o contrato (no es la fecha de cierre).",
            "carreras_objetivo": "Puedes elegir varias carreras.",
            "vacantes": "Número referencial de puestos disponibles.",
            "banda_salarial_min": "Opcional. Muestra el rango y sube tu transparencia.",
            "banda_salarial_max": "Opcional. Complétalo junto con el mínimo para mostrar el rango.",
            "medio_postulacion": "Un enlace de postulación (https://…) o un correo para recibir CVs "
            "(ej. rrhh@empresa.pe). El postulante saldrá a este medio; CONECTA no gestiona la selección.",
            "email_contacto": "Correo de contacto de la empresa (anti-spam y trazabilidad).",
        }
