# Librerías estándar
from pathlib import Path

# FastAPI
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Directorios de plantillas y archivos estáticos
CURRENT_DIR = Path(__file__).parent.resolve()
TEMPLATE_DIR = CURRENT_DIR / "templates"
STATIC_DIR = CURRENT_DIR / "static"

# Configuración de Jinja2Templates
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/", summary="Renderizar la página de inicio")
async def get_home_frontend(request: Request):
    """
    Renderiza la página de inicio usando Jinja2.

    - **Parámetros**:
        - `request` (Request): Objeto de solicitud HTTP.

    - **Retorna**:
        - `TemplateResponse`: Renderiza la plantilla `index.html`.
    """

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Home"
        }
    )