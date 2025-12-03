# ─────────────────
# 📦 Importaciones
# ─────────────────
# 🐍 Librería estándar
from typing import cast

# 🧩 Terceros
from fastapi import Request, HTTPException, status

# 🏗️  Módulos internos de la aplicación
from app.libraries.TheaterHandler import TheaterHandler

def get_theater(request: Request) -> TheaterHandler:
    theater_handler = getattr(request.app.state, 'theater_handler', None)
    if theater_handler is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Theater no inicializado",
        )

    return cast(TheaterHandler, theater_handler)