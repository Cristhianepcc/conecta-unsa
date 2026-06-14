"""Adapters de allauth: enrutan según rol tras autenticar (auth-roles.md §2)."""

from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .services import asegurar_perfil, resolver_rol_y_destino


class CuentaAdapter(DefaultAccountAdapter):
    """El destino post-login lo decide la identidad, no la pestaña elegida."""

    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated:
            return reverse(resolver_rol_y_destino(user))
        return super().get_login_redirect_url(request)


class AdaptadorSocial(DefaultSocialAccountAdapter):
    """Asegura el Perfil al registrarse vía Google (primer ingreso)."""

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        asegurar_perfil(user)
        return user
