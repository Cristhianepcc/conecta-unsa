from django import forms


class ConsentimientoForm(forms.Form):
    """Consentimiento informado de datos (Ley 29733 / NFR-PRIV-1)."""

    consentimiento = forms.BooleanField(
        required=True,
        label="Acepto el tratamiento de mis datos personales conforme a la Ley 29733 "
        "y la Política de Privacidad de CONECTA UNSA.",
        error_messages={"required": "Debes aceptar el tratamiento de datos para continuar."},
    )
