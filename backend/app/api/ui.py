# app/api/ui.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db.session import get_session
from app.core.plugins.registry import get_manifest
from app.core.plugins.models import Plugin, TenantPlugin

router = APIRouter(prefix="/tenants/{tenant_id}/ui", tags=["ui"])


@router.get("/menu")
async def get_menu(
    tenant_id: str,
    session: AsyncSession = Depends(get_session),
):
    # plugins activés pour le tenant
    rows = await session.execute(
        select(Plugin.key)
        .join(TenantPlugin, TenantPlugin.plugin_id == Plugin.id)
        .where(TenantPlugin.tenant_id == tenant_id, TenantPlugin.is_enabled == True)
    )
    enabled_keys = [r[0] for r in rows.all()]

    pages: list[dict] = []
    for key in enabled_keys:
        m = get_manifest(key)
        if not m or not m.ui_pages:
            continue
        for p in m.ui_pages:
            pages.append({**p, "plugin": key})

    # tri
    pages.sort(key=lambda x: (x.get("order", 9999), x.get("label", "")))
    return {"tenant_id": tenant_id, "pages": pages}
