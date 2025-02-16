from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.routers import router, home_static_dir

app = FastAPI()

app.include_router(router)
app.mount("/static", StaticFiles(directory=home_static_dir), name="static")