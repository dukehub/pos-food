from sqlalchemy import select

from app.core.db.base import Base
from app.core.db.session import AsyncSessionLocal, engine
from app.core.plugins.models import Plugin
from app.core.plugins.registry import list_manifests


class PluginRuntime:
    async def sync_database(self) -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        async with AsyncSessionLocal() as session:
            for manifest in list_manifests():
                plugin = (
                    await session.execute(
                        select(Plugin).where(Plugin.key == manifest.key)
                    )
                ).scalar_one_or_none()
                if plugin:
                    plugin.name = manifest.name
                    plugin.description = manifest.description
                    plugin.version = manifest.version
                    plugin.is_active = True
                else:
                    session.add(
                        Plugin(
                            key=manifest.key,
                            name=manifest.name,
                            description=manifest.description,
                            version=manifest.version,
                            is_active=True,
                        )
                    )
            await session.commit()
