from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.plugins.models import Plugin, TenantPlugin


async def is_plugin_enabled(
    session: AsyncSession,
    tenant_id: str,
    plugin_key: str,
) -> bool:
    plugin = (
        await session.execute(select(Plugin).where(Plugin.key == plugin_key))
    ).scalar_one_or_none()
    if not plugin:
        return False

    tenant_plugin = (
        await session.execute(
            select(TenantPlugin).where(
                TenantPlugin.tenant_id == tenant_id,
                TenantPlugin.plugin_id == plugin.id,
            )
        )
    ).scalar_one_or_none()

    return tenant_plugin.is_enabled if tenant_plugin else False
