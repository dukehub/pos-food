from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.setup_ui import router as setup_ui_router
from app.core.config.settings import settings
from app.core.plugins.bootstrap import include_plugin_routers
from app.core.plugins.loader import AsyncPluginLoader
from app.core.plugins.runtime import PluginRuntime
from app.core.tenancy.middleware import TenancyMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Core
    from app.core.events import event_bus
    # We could trigger 'app.startup' event here if we wanted
    
    loader = AsyncPluginLoader()
    await loader.load_all()
    include_plugin_routers(app)

    runtime = PluginRuntime()
    await runtime.sync_database()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(TenancyMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:8000", "tauri://localhost", "https://tauri.localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(setup_ui_router)
    app.include_router(api_router)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
