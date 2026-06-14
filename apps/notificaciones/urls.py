from django.urls import path

from . import views

app_name = "notificaciones"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("marcar-leidas/", views.marcar_todas_leidas, name="marcar_leidas"),
]
