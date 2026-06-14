from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("como-funciona/", views.como_funciona, name="como_funciona"),
    path("privacidad/", views.privacidad, name="privacidad"),
    path("terminos/", views.terminos, name="terminos"),
    path("panel-admin/", views.panel_admin, name="panel_admin"),
    path("panel-admin/aprobar-lote/", views.aprobar_lote, name="aprobar_lote"),
    path("panel-admin/convocatoria/<int:pk>/", views.revisar_convocatoria,
         name="revisar_convocatoria"),
]
