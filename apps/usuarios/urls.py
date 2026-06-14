from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("login/empresa/", views.login_empresa, name="login_empresa"),
    path("post-login/", views.post_login, name="post_login"),
    path("logout/", views.logout_view, name="logout"),
    path("completar-perfil/", views.completar_perfil, name="completar_perfil"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
