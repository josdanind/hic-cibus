# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería Estándar
from fastapi import HTTPException, status

# ─────────────────────────────
# ⚠️ ERRORES 4XX - CLIENTE
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

def unsupported_media_type(detail: str = "Tipo de contenido no soportado") -> HTTPException:
    """
    415 Unsupported Media Type:
    El servidor no puede procesar la solicitud porque el tipo de contenido
    especificado en la cabecera 'Content-Type' no es soportado por el endpoint.
    Por ejemplo, se espera 'application/json' pero se recibe 'text/plain'.
    """
    return HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=detail
    )

# ─────────────────────────────
# 💥 ERRORES 5XX - SERVIDOR
# ─────────────────────────────

def internal_server_error(detail: str = "Error interno del servidor") -> HTTPException:
    """
    500 Internal Server Error:
    El servidor encontró una condición inesperada que le impidió cumplir con la solicitud.
    Este error es genérico y debe usarse solo cuando no hay un código más específico.
    Evita revelar detalles técnicos para no comprometer la seguridad del sistema.
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail
    )