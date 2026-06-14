"""URLs raíz de CONECTA UNSA.

La fundación (00) deja el `include()` de cada app listo para que las features
posteriores solo agreguen rutas dentro de su propia app (ver specs/plan-paralelo.md §2).
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve as media_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    # Media subida por usuarios (logos/banners). Se sirve desde el volumen
    # persistente (MEDIA_ROOT) en dev y prod, sin servicios externos. Para alto
    # tráfico, anteponer un CDN/Nginx delante de esta ruta.
    re_path(
        r"^media/(?P<path>.*)$",
        media_serve,
        {"document_root": settings.MEDIA_ROOT},
        name="media",
    ),
    path("accounts/", include("allauth.urls")),
    # PWA: manifest e instalación. El service worker se sirve desde la raíz
    # ("/sw.js") para que su alcance (scope) abarque todo el sitio.
    path(
        "manifest.webmanifest",
        TemplateView.as_view(
            template_name="pwa/manifest.webmanifest",
            content_type="application/manifest+json",
        ),
        name="pwa_manifest",
    ),
    path(
        "sw.js",
        TemplateView.as_view(
            template_name="pwa/sw.js",
            content_type="application/javascript",
        ),
        name="pwa_sw",
    ),
    # Apps del proyecto
    path("api/", include("apps.integraciones.urls")),
    path("taxonomia/", include("apps.taxonomia.urls")),
    path("usuarios/", include("apps.usuarios.urls")),
    path("empresas/", include("apps.empresas.urls")),
    path("convocatorias/", include("apps.convocatorias.urls")),
    path("matching/", include("apps.matching.urls")),
    path("notificaciones/", include("apps.notificaciones.urls")),
    # Núcleo / público (debe ir al final por capturar la raíz "")
    path("", include("apps.core.urls")),
]
