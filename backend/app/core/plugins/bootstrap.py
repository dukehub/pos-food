from fastapi import FastAPI, Depends
from app.core.config.settings import settings
from app.core.plugins.registry import list_manifests
from app.core.tenancy.plugins_router import router as tenancy_plugins_router
from app.core.plugins.dependencies import require_plugin_enabled


def include_core_routers(app: FastAPI) -> None:
    app.include_router(tenancy_plugins_router)  # ce router a déjà /api/... dans son prefix


def include_plugin_routers(app: FastAPI) -> None:
    for manifest in list_manifests():
        if manifest.router:
            # Convention: /api/plugins/<slug>
            # Best practice: Guard with simple dependency
            app.include_router(
                manifest.router, 
                prefix=f"{settings.api_prefix}/plugins/{manifest.key}",
                dependencies=[Depends(require_plugin_enabled(manifest.key))],
                tags=[manifest.key]
            )
