"""URLs raíz de CONECTA UNSA.

La fundación (00) deja el `include()` de cada app listo para que las features
posteriores solo agreguen rutas dentro de su propia app (ver specs/plan-paralelo.md §2).
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    # Apps del proyecto
    path("taxonomia/", include("apps.taxonomia.urls")),
    path("usuarios/", include("apps.usuarios.urls")),
    path("empresas/", include("apps.empresas.urls")),
    path("convocatorias/", include("apps.convocatorias.urls")),
    path("matching/", include("apps.matching.urls")),
    path("notificaciones/", include("apps.notificaciones.urls")),
    # Núcleo / público (debe ir al final por capturar la raíz "")
    path("", include("apps.core.urls")),
]
