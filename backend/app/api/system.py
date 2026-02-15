from fastapi import APIRouter

from app.core.config.settings import settings
from app.core.plugins.registry import list_manifests

router = APIRouter(prefix="/system", tags=["system"])


@router.get("")
async def system_info() -> dict:
    plugins = [
        {
            "key": manifest.key,
            "name": manifest.name,
            "version": manifest.version,
            "description": manifest.description,
        }
        for manifest in list_manifests()
    ]
    return {
        "status": "ok",
        "env": settings.env,
        "plugins": plugins,
    }
