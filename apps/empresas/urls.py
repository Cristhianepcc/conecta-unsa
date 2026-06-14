from django.urls import path

from . import views

app_name = "empresas"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("publicar/", views.publicar, name="publicar"),
    path("perfil/", views.editar_perfil, name="editar_perfil"),
    path("convocatoria/<int:pk>/editar/", views.editar_convocatoria, name="editar"),
    path("registro/", views.registro, name="registro"),
    path("registro/exito/", views.registro_exito, name="registro_exito"),
]
