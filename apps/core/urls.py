from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("panel-admin/", views.panel_admin, name="panel_admin"),
]
