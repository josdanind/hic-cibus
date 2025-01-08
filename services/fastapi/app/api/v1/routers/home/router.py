# Standard Library
from pathlib import Path

# FastAPI
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

CURRENT_DIR = Path(__file__).parent.resolve()
TEMPLATE_DIR = CURRENT_DIR / "templates"
STATIC_DIR = CURRENT_DIR / "static"

templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/")
async def get_home_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})