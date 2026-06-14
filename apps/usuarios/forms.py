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
    """Primer ingreso: DNI (valida con la UNSA) o carrera + estado autodeclarados + consentimiento.

    `carrera`/`estado_academico` son opcionales aquí: si el DNI valida contra el
    padrón UNSA, la vista los toma del resultado verificado; si no, exige que el
    egresado los declare (validación en la vista, no en el form).
    """

    dni = forms.CharField(
        label="DNI",
        max_length=8,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingresa tu DNI — validaremos tu carrera con la UNSA",
                "inputmode": "numeric",
                "pattern": "[0-9]{8}",
                "autocomplete": "off",
            }
        ),
    )
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activa=True), label="Carrera",
        empty_label="Selecciona tu carrera", required=False,
    )
    estado_academico = forms.ChoiceField(
        choices=constants.ESTADOS_ACADEMICOS, label="Estado académico", required=False,
    )
    consentimiento = forms.BooleanField(
        required=True,
        label="Acepto el tratamiento de mis datos personales (Ley 29733).",
        error_messages={"required": "Debes aceptar el tratamiento de datos para continuar."},
    )
    consentimiento_matching = forms.BooleanField(
        required=True,
        label="Autorizo el uso de mi carrera y credenciales para el matching inteligente.",
        error_messages={
            "required": "Debes autorizar el uso de tus datos para el matching para continuar."
        },
    )
    consentimiento_credencial_publica = forms.BooleanField(
        required=False,
        label="Quiero activar mi credencial pública (opcional; puedo cambiarlo luego).",
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
