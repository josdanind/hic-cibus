# Librerías estándar
from contextlib import asynccontextmanager

# FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Routers y archivos estáticos
from app.api.v1.routers import router, home_static_dir


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Esta función se ejecuta cuando la aplicación FastAPI inicia y termina.
    """

    yield

app = FastAPI(
    title="hic-cibus",
    description="Frontend hic-cibus",
    version="0.1.0",
    lifespan=lifespan
)


# Inclusión de routers en la aplicación
app.include_router(router)

# Montaje de archivos estáticos (CSS, JS, imágenes, etc.)
app.mount("/static", StaticFiles(directory=home_static_dir), name="static")