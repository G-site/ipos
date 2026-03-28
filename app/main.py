from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_title, description=settings.app_description)
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    app.include_router(router)
    return app


app = create_app()
