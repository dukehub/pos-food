"""Plugin lifecycle manager (install/upgrade per tenant)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import anyio
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.settings import settings
from app.core.plugins.models import Plugin, TenantPlugin
from app.core.plugins.registry import get_manifest


@dataclass
class PluginApplyResult:
    installed: bool
    upgraded: bool
    from_version: Optional[str]
    to_version: str


class PluginLifecycleManager:
    def __init__(self, session: AsyncSession, database_url: str | None = None):
        self.session = session
        self.database_url = database_url or settings.database_url

    async def ensure_installed_for_tenant(
        self, tenant_id: str, plugin_key: str
    ) -> PluginApplyResult:
        manifest = get_manifest(plugin_key)
        if not manifest:
            raise RuntimeError(f"Manifest not loaded for plugin: {plugin_key}")

        to_version = manifest.version

        # 1) Migrate
        if manifest.migrations_path:
            await self._run_plugin_migrations(plugin_key, manifest.migrations_path)

        # 2) Link tenant/plugin
        plugin = await self._get_plugin_row(plugin_key)
        link = await self._get_tenant_link(tenant_id, plugin.id)
        from_version = link.installed_version
        installed = from_version is None
        upgraded = from_version is not None and from_version != to_version
        link.is_enabled = True

        # 3) Seed (idempotent)
        if manifest.seed:
            await manifest.seed(self.session, tenant_id)

        # 4) Persist install state
        link.installed_version = to_version
        link.installed_at = datetime.now(timezone.utc)
        await self.session.flush()

        return PluginApplyResult(
            installed=installed,
            upgraded=upgraded,
            from_version=from_version,
            to_version=to_version,
        )

    async def _get_plugin_row(self, plugin_key: str) -> Plugin:
        from sqlalchemy import select

        res = await self.session.execute(select(Plugin).where(Plugin.key == plugin_key))
        return res.scalar_one()

    async def _get_tenant_link(self, tenant_id: str, plugin_id: int) -> TenantPlugin:
        from sqlalchemy import select

        res = await self.session.execute(
            select(TenantPlugin).where(
                TenantPlugin.tenant_id == tenant_id, TenantPlugin.plugin_id == plugin_id
            )
        )
        link = res.scalar_one_or_none()
        if not link:
            link = TenantPlugin(tenant_id=tenant_id, plugin_id=plugin_id, is_enabled=True)
            self.session.add(link)
        return link

    async def _run_plugin_migrations(self, plugin_key: str, migrations_path: str) -> None:
        import importlib.util
        import os

        # Resolve dotted path to filesystem path when needed.
        if not os.path.exists(migrations_path):
            try:
                spec = importlib.util.find_spec(migrations_path)
                if spec and spec.submodule_search_locations:
                    migrations_path = spec.submodule_search_locations[0]
            except Exception:
                pass

        cfg = Config()
        cfg.set_main_option("script_location", migrations_path)

        # Skip when plugin has no migration scripts.
        versions_dir = os.path.join(migrations_path, "versions")
        if not os.path.exists(versions_dir):
            return
        revision_files = [
            f
            for f in os.listdir(versions_dir)
            if f.endswith(".py") and f != "__init__.py"
        ]
        if not revision_files:
            return

        # Use sync driver URL for Alembic.
        url = self.database_url.replace("+asyncpg", "").replace("+aiosqlite", "")
        cfg.set_main_option("sqlalchemy.url", url)
        cfg.set_main_option("version_table", f"alembic_version__{plugin_key}")

        await _run_alembic_upgrade(cfg, "head")


async def _run_alembic_upgrade(cfg: Config, revision: str) -> None:
    def worker() -> None:
        try:
            command.upgrade(cfg, revision)
        except Exception as exc:
            # SQLite setup flow may create tables first via metadata.create_all.
            # In that case, stamp plugin head so lifecycle can continue idempotently.
            url = (cfg.get_main_option("sqlalchemy.url") or "").lower()
            if url.startswith("sqlite") and "already exists" in str(exc).lower():
                command.stamp(cfg, revision)
                return
            raise

    await anyio.to_thread.run_sync(worker)
