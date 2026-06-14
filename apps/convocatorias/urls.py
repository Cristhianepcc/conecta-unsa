from django.urls import path

from . import views

app_name = "convocatorias"

urlpatterns = [
    path("<int:pk>/", views.detalle, name="detalle"),
    path("<int:pk>/postular/", views.postular, name="postular"),
    path("<int:pk>/guardar/", views.guardar, name="guardar"),
]
