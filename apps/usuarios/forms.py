from django import forms

from apps.taxonomia.models import Carrera

from .models import (
    FRECUENCIAS,
    Credencial,
    PerfilTalento,
)
from apps.core import constants


class ConsentimientoForm(forms.Form):
    """Consentimiento informado de datos (Ley 29733 / NFR-PRIV-1)."""

    consentimiento = forms.BooleanField(
        required=True,
        label="Acepto el tratamiento de mis datos personales conforme a la Ley 29733 "
        "y la Política de Privacidad de CONECTA UNSA.",
        error_messages={"required": "Debes aceptar el tratamiento de datos para continuar."},
    )


class CompletarPerfilForm(forms.Form):
    """Primer ingreso: carrera + estado académico (autodeclarado en demo) + consentimiento."""

    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activa=True), label="Carrera",
        empty_label="Selecciona tu carrera",
    )
    estado_academico = forms.ChoiceField(
        choices=constants.ESTADOS_ACADEMICOS, label="Estado académico"
    )
    consentimiento = forms.BooleanField(
        required=True,
        label="Acepto el tratamiento de mis datos personales (Ley 29733).",
        error_messages={"required": "Debes aceptar el tratamiento de datos para continuar."},
    )


class PreferenciasForm(forms.ModelForm):
    """Preferencias del egresado: carrera, estado, carreras afines y frecuencia.

    Los tipos (preferido/normal/silenciado) se manejan como matriz tri-estado en la
    vista/plantilla (no como campos del form), para evitar estados contradictorios.
    """

    frecuencia = forms.ChoiceField(choices=FRECUENCIAS, label="Frecuencia de notificación")

    class Meta:
        model = PerfilTalento
        fields = ["carrera", "estado_academico", "carreras_extra", "frecuencia"]
        widgets = {"carreras_extra": forms.CheckboxSelectMultiple}


class CredencialForm(forms.ModelForm):
    """Alta/edición de credenciales autodeclaradas."""

    class Meta:
        model = Credencial
        fields = ["tipo", "detalle", "visible_para_empresas"]
