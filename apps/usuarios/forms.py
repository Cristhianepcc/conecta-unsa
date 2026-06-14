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
    """Preferencias del egresado (carreras extra, silenciar, tipos preferidos, frecuencia)."""

    categorias_silenciadas = forms.MultipleChoiceField(
        choices=constants.TIPOS_CONVOCATORIA, required=False,
        widget=forms.CheckboxSelectMultiple, label="Silenciar tipos",
    )
    tipos_preferidos = forms.MultipleChoiceField(
        choices=constants.TIPOS_CONVOCATORIA, required=False,
        widget=forms.CheckboxSelectMultiple, label="Tipos preferidos",
    )
    frecuencia = forms.ChoiceField(choices=FRECUENCIAS, label="Frecuencia de notificación")

    class Meta:
        model = PerfilTalento
        fields = ["carrera", "estado_academico", "carreras_extra",
                  "categorias_silenciadas", "tipos_preferidos", "frecuencia"]
        widgets = {"carreras_extra": forms.SelectMultiple}


class CredencialForm(forms.ModelForm):
    """Alta/edición de credenciales autodeclaradas."""

    class Meta:
        model = Credencial
        fields = ["tipo", "detalle", "visible_para_empresas"]
