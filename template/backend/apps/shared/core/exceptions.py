from __future__ import annotations

from rest_framework import status
from rest_framework.exceptions import APIException


class BusinessLogicError(APIException):
    """Error de lógica de negocio. Lanzar desde services."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Error en la operación solicitada."
    default_code = "business_logic_error"


class NotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Recurso no encontrado."
    default_code = "not_found"


class PermissionDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "No tienes permiso para realizar esta acción."
    default_code = "permission_denied"


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflicto con el estado actual del recurso."
    default_code = "conflict"
