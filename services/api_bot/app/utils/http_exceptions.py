# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería Estándar
from fastapi import HTTPException, status

# ─────────────────────────────
# 🚫 ERRORES GENERALES
# ─────────────────────────────

def not_found(detail: str = "Recurso no encontrado") -> HTTPException:
    """
    404 Not Found:
    El recurso solicitado no existe o no se pudo encontrar.
    Se utiliza cuando el cliente pide un recurso válido pero inexistente.
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )

def bad_request(detail: str = "Solicitud inválida") -> HTTPException:
    """
    400 Bad Request:
    La solicitud es incorrecta o malformada.
    Se usa cuando hay errores de lógica o formato antes de validar los datos.
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )

def unauthorized(detail: str = "No autorizado") -> HTTPException:
    """
    401 Unauthorized:
    El cliente no está autenticado o el token de acceso es inválido.
    Se usa cuando se requiere autenticación y no se ha proporcionado.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )

def forbidden(detail: str = "Acceso denegado") -> HTTPException:
    """
    403 Forbidden:
    El cliente está autenticado pero no tiene permisos para acceder al recurso.
    Se usa cuando se niega el acceso por falta de privilegios.
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )

def conflict(detail: str = "Conflicto con el estado actual del recurso") -> HTTPException:
    """
    409 Conflict:
    La solicitud no puede completarse debido a un conflicto con el estado actual del servidor.
    Se usa en casos como duplicados, condiciones de carrera o versiones en conflicto.
    """
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail
    )

def unprocessable_entity(detail: str = "Entidad no procesable") -> HTTPException:
    """
    422 Unprocessable Entity:
    La solicitud es sintácticamente correcta, pero los datos no cumplen las validaciones requeridas.
    FastAPI lanza este error automáticamente cuando fallan validaciones con Pydantic.
    """
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail
    )