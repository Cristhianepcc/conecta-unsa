from django.urls import path

from . import views

app_name = "integraciones"

urlpatterns = [
    path("validar-dni/", views.validar_dni, name="validar_dni"),
]
