"""Control de acceso por rol (NFR-SEC-1). Decoradores y mixins reutilizables.

Si una vista requiere un rol y el usuario no lo tiene, se deniega (403).
"""

from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .models import ROL_ADMIN, ROL_EGRESADO, ROL_RECLUTADOR
from .services import asegurar_perfil


def _rol_actual(user) -> str | None:
    if not user.is_authenticated:
        return None
    return asegurar_perfil(user).rol


def rol_requerido(*roles):
    """Decorador de vista función: exige uno de los roles dados."""

    def decorador(view):
        @wraps(view)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if _rol_actual(request.user) not in roles:
                raise PermissionDenied("No tienes permiso para acceder a esta sección.")
            return view(request, *args, **kwargs)

        return _wrapped

    return decorador


admin_required = rol_requerido(ROL_ADMIN)
empresa_required = rol_requerido(ROL_RECLUTADOR)
egresado_required = rol_requerido(ROL_EGRESADO)


class RolRequeridoMixin:
    """Mixin para CBVs: define `roles_permitidos`."""

    roles_permitidos: tuple = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if _rol_actual(request.user) not in self.roles_permitidos:
            raise PermissionDenied("No tienes permiso para acceder a esta sección.")
        return super().dispatch(request, *args, **kwargs)


class AdminRequeridoMixin(RolRequeridoMixin):
    roles_permitidos = (ROL_ADMIN,)


class EmpresaRequeridoMixin(RolRequeridoMixin):
    roles_permitidos = (ROL_RECLUTADOR,)


class EgresadoRequeridoMixin(RolRequeridoMixin):
    roles_permitidos = (ROL_EGRESADO,)
