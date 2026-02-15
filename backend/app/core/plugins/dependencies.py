from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id
from app.core.plugins.models import TenantPlugin, Plugin


def require_plugin_enabled(plugin_key: str):
    async def dependency(session: AsyncSession = Depends(get_session)):
        tenant_id = get_tenant_id()
        # On suppose que 'public' ne peut pas accéder aux plugins (ou policy à affiner)
        if not tenant_id or tenant_id == "public":
            raise HTTPException(status_code=403, detail="Tenant context required for plugin access")

        # Vérifie si le plugin est activé pour ce tenant
        # Optimization: pourrait être cache avec Redis
        stmt = (
            select(TenantPlugin.is_enabled)
            .join(Plugin, Plugin.id == TenantPlugin.plugin_id)
            .where(
                TenantPlugin.tenant_id == tenant_id,
                Plugin.key == plugin_key
            )
        )
        res = await session.execute(stmt)
        is_enabled = res.scalar_one_or_none()

        if not is_enabled:
            # 404 pour ne pas leaker l'existence, ou 403 Forbidden
            # Le test attend 404 ou 403.
            raise HTTPException(status_code=404, detail=f"Plugin '{plugin_key}' not enabled or found")

    return dependency
