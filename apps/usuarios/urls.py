from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    # 02 — Autenticación
    path("login/", views.login_view, name="login"),
    path("login/empresa/", views.login_empresa, name="login_empresa"),
    path("demo/<str:rol>/", views.demo_login, name="demo_login"),
    path("post-login/", views.post_login, name="post_login"),
    path("logout/", views.logout_view, name="logout"),
    path("completar-perfil/", views.completar_perfil, name="completar_perfil"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("guardadas/", views.guardadas, name="guardadas"),
    path("historial/", views.historial, name="historial"),
    path("ayuda/", views.ayuda, name="ayuda"),
    # 07 — Perfil y credencial
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/credencial/<int:credencial_id>/eliminar/", views.eliminar_credencial,
         name="eliminar_credencial"),
    path("perfil/credencial-publica/", views.credencial_config, name="credencial_config"),
    path("credencial/<slug:slug>/", views.credencial_publica, name="credencial_publica"),
]
