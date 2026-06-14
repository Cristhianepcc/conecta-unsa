"""Helpers de acceso a la configuración-como-datos."""

from decimal import Decimal, InvalidOperation

from .models import ParametroLegal


def get_parametro(clave: str, default: str | None = None) -> str | None:
    """Devuelve el valor (str) de un ParametroLegal, o `default` si no existe."""
    obj = ParametroLegal.objects.filter(clave=clave).first()
    return obj.valor if obj else default


def get_parametro_decimal(clave: str, default: Decimal = Decimal("0")) -> Decimal:
    valor = get_parametro(clave)
    if valor is None:
        return default
    try:
        return Decimal(valor)
    except (InvalidOperation, ValueError):
        return default


def get_parametro_int(clave: str, default: int = 0) -> int:
    valor = get_parametro(clave)
    try:
        return int(valor) if valor is not None else default
    except (ValueError, TypeError):
        return default
