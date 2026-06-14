from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.usuarios"
    verbose_name = "Usuarios y perfiles"

    def ready(self):
        from . import signals  # noqa: F401  (registra la señal post_save)
