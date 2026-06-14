from django.urls import path

from . import views

app_name = "empresas"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("registro/", views.registro, name="registro"),
]
