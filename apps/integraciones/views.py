"""Endpoints de interoperabilidad (Eje 2).

`validar_dni` es el indicador de validación en tiempo real: el frontend consulta
este endpoint mientras el egresado escribe su DNI y muestra si la identidad
proviene de la base académica de la UNSA.
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .padron import consultar_dni, dni_valido


@login_required
@require_http_methods(["GET"])
def validar_dni(request):
    """GET /api/validar-dni/?dni=NNNNNNNN

    Respuestas:
      400 {"estado":"formato_invalido","mensaje":...}
      200 {"estado":"no_encontrado"}
      200 {"estado":"validado","nombres":...,"carrera":...,"carrera_id":...,
           "estado_academico":...,"fuente":"UNSA"}
    """
    dni = (request.GET.get("dni") or "").strip()
    if not dni_valido(dni):
        return JsonResponse(
            {"estado": "formato_invalido", "mensaje": "El DNI debe tener 8 dígitos."},
            status=400,
        )

    resultado = consultar_dni(dni)
    if resultado is None:
        return JsonResponse({"estado": "no_encontrado"})

    return JsonResponse(
        {
            "estado": "validado",
            "nombres": resultado.nombres,
            "carrera": resultado.carrera,
            "carrera_id": resultado.carrera_id,
            "estado_academico": resultado.estado_academico,
            "fuente": resultado.fuente,
        }
    )
