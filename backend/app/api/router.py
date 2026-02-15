
from fastapi import APIRouter

from app.api import auth, plugins_runtime, system, setup, ui
from app.core.config.settings import settings

api_router = APIRouter(prefix=settings.api_prefix)

api_router.include_router(system.router)
api_router.include_router(setup.router)
api_router.include_router(plugins_runtime.router)
api_router.include_router(auth.router)
api_router.include_router(ui.router)
