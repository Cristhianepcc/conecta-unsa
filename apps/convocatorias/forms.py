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
        }
