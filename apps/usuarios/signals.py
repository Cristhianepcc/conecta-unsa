"""Crea automáticamente un Perfil para cada usuario nuevo."""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="crear_perfil_usuario")
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(user=instance)
