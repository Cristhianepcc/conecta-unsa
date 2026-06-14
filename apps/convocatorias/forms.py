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
            "descripcion": forms.Textarea(attrs={"rows": 5}),
            "beneficios": forms.Textarea(attrs={"rows": 3}),
            "cronograma": forms.Textarea(attrs={"rows": 3}),
            "medio_postulacion": forms.TextInput(
                attrs={"placeholder": "https://empresa.pe/empleos  ó  rrhh@empresa.pe"}
            ),
        }
        help_texts = {
            "medio_postulacion": "Un enlace de postulación (https://…) o un correo para recibir CVs "
            "(ej. rrhh@empresa.pe). El postulante saldrá a este medio; CONECTA no gestiona la selección.",
            "email_contacto": "Correo de contacto de la empresa (anti-spam y trazabilidad).",
        }
