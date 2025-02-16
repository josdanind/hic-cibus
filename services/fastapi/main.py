# FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Routers y archivos estáticos
from app.api.v1.routers import router, home_static_dir

app = FastAPI(
    title="Plantila de FastAPI",
    description="Plantilla de proyecto FastAPI con estructura modular.",
    version="0.1.0",
)

# Inclusión de routers en la aplicación
app.include_router(router)

# Montaje de archivos estáticos (CSS, JS, imágenes, etc.)
app.mount("/static", StaticFiles(directory=home_static_dir), name="static")