from django import forms
from django.contrib.auth import get_user_model

from .models import Empresa, Reclutador

User = get_user_model()


class EmpresaForm(forms.ModelForm):
    """Bloque A — Información de la empresa."""

    class Meta:
        model = Empresa
        fields = [
            "ruc", "razon_social", "nombre_comercial", "tipo", "ciiu",
            "telefono", "direccion", "web", "linkedin",
            "logo_img", "banner_img", "video_url", "descripcion",
        ]
        widgets = {
            "logo_img": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "banner_img": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }


class EditarEmpresaForm(forms.ModelForm):
    """Edición del perfil público de la empresa (el RUC es la identidad, no editable)."""

    class Meta:
        model = Empresa
        fields = [
            "razon_social", "nombre_comercial", "tipo", "ciiu",
            "telefono", "direccion", "web", "linkedin",
            "logo_img", "banner_img", "video_url", "descripcion",
        ]
        widgets = {
            "logo_img": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "banner_img": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }


class ReclutadorForm(forms.ModelForm):
    """Bloque B — Reclutador asignado + credenciales de su cuenta."""

    username = forms.CharField(label="Usuario", max_length=150)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Repite la contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Reclutador
        fields = ["dni", "nombres", "ap_paterno", "ap_materno", "cargo", "email", "telefono"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ese usuario ya está en uso.")
        return username

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned
