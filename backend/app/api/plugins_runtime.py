from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.plugins.lifecycle import PluginLifecycleManager
from app.core.db.session import get_session
from app.core.plugins.models import Plugin, TenantPlugin
from app.core.plugins.registry import (
    PluginDependencyError,
    get_manifest,
    list_manifests,
    validate_enabled_dependencies,
)

# IMPORTANT:
# - api_router in app/api/router.py already has prefix=settings.api_prefix ("/api")
# - therefore this router must NOT start with "/api" again, otherwise you'd get "/api/api/...".
router = APIRouter(prefix="/tenants", tags=["plugins"])


def _unknown_plugin(plugin_key: str) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail={"error": "unknown_plugin", "plugin": plugin_key},
    )


@router.get("/{tenant_id}/plugins")
async def list_plugins(
    tenant_id: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    plugins = (await session.execute(select(Plugin))).scalars().all()
    tenant_plugins = (
        await session.execute(select(TenantPlugin).where(TenantPlugin.tenant_id == tenant_id))
    ).scalars().all()

    tenant_map = {tp.plugin_id: tp for tp in tenant_plugins}

    items = []
    for plugin in plugins:
        tenant_link = tenant_map.get(plugin.id)
        enabled = tenant_link.is_enabled if tenant_link else False

        manifest = get_manifest(plugin.key)
        items.append(
            {
                "key": plugin.key,
                "name": plugin.name,
                "description": plugin.description,
                "version": plugin.version,
                "enabled": enabled,
                "requires": (manifest.requires if manifest and manifest.requires else []),
                "manifest_loaded": manifest is not None,
                "ui_pages": (manifest.ui_pages if manifest and manifest.ui_pages else []),
            }
        )

    return {"tenant_id": tenant_id, "plugins": items}


@router.post("/{tenant_id}/plugins/{plugin_key}:enable")
async def enable_plugin(
    tenant_id: str,
    plugin_key: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    plugin = (
        await session.execute(select(Plugin).where(Plugin.key == plugin_key))
    ).scalar_one_or_none()
    if not plugin:
        raise _unknown_plugin(plugin_key)

    # 1) Current enabled keys for tenant
    enabled_rows = (
        await session.execute(
            select(Plugin.key)
            .join(TenantPlugin, TenantPlugin.plugin_id == Plugin.id)
            .where(
                TenantPlugin.tenant_id == tenant_id,
                TenantPlugin.is_enabled == True,  # noqa: E712
            )
        )
    ).all()
    enabled_keys = {row[0] for row in enabled_rows}

    # 2) Future state after activation
    new_enabled = set(enabled_keys)
    new_enabled.add(plugin_key)

    # 3) Validate manifest dependencies
    try:
        validate_enabled_dependencies(new_enabled, list_manifests(sorted_=False))
    except PluginDependencyError:
        manifest = get_manifest(plugin_key)
        missing = []
        if manifest and manifest.requires:
            missing = [dep for dep in manifest.requires if dep not in new_enabled]

        raise HTTPException(
            status_code=409,
            detail={
                "error": "missing_dependencies",
                "plugin": plugin_key,
                "missing": missing,
                "hint": "Enable required plugin(s) first.",
            },
        )

    try:
        # NEW: install/upgrade + seed
        lifecycle = PluginLifecycleManager(session)
        apply_res = await lifecycle.ensure_installed_for_tenant(tenant_id, plugin_key)
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    manifest = get_manifest(plugin_key)
    return {
        "tenant_id": tenant_id,
        "plugin": plugin_key,
        "enabled": True,
        "manifest_loaded": manifest is not None,
        "installed": apply_res.installed,
        "upgraded": apply_res.upgraded,
        "from_version": apply_res.from_version,
        "to_version": apply_res.to_version,
    }


@router.post("/{tenant_id}/plugins/{plugin_key}:disable")
async def disable_plugin(
    tenant_id: str,
    plugin_key: str,
    session: AsyncSession = Depends(get_session),
) -> dict:
    plugin = (
        await session.execute(select(Plugin).where(Plugin.key == plugin_key))
    ).scalar_one_or_none()
    if not plugin:
        raise _unknown_plugin(plugin_key)

    tenant_plugin = (
        await session.execute(
            select(TenantPlugin).where(
                TenantPlugin.tenant_id == tenant_id,
                TenantPlugin.plugin_id == plugin.id,
            )
        )
    ).scalar_one_or_none()

    if not tenant_plugin:
        tenant_plugin = TenantPlugin(tenant_id=tenant_id, plugin_id=plugin.id, is_enabled=False)
        session.add(tenant_plugin)
    else:
        # Validate reverse dependencies before disabling.
        enabled_rows = (
            await session.execute(
                select(Plugin.key)
                .join(TenantPlugin, TenantPlugin.plugin_id == Plugin.id)
                .where(
                    TenantPlugin.tenant_id == tenant_id,
                    TenantPlugin.is_enabled == True,  # noqa: E712
                )
            )
        ).all()
        enabled_keys = {row[0] for row in enabled_rows}
        next_enabled = set(enabled_keys)
        next_enabled.discard(plugin_key)

        manifests = list_manifests(sorted_=False)
        try:
            validate_enabled_dependencies(next_enabled, manifests)
        except PluginDependencyError:
            blocked_by = []
            manifests_by_key = {m.key: m for m in manifests}
            for key in next_enabled:
                manifest = manifests_by_key.get(key)
                if manifest and plugin_key in (manifest.requires or []):
                    blocked_by.append(key)

            raise HTTPException(
                status_code=409,
                detail={
                    "error": "plugin_required_by_enabled_plugins",
                    "plugin": plugin_key,
                    "required_by": sorted(blocked_by),
                    "hint": "Disable dependent plugin(s) first.",
                },
            )

        tenant_plugin.is_enabled = False

    await session.commit()
    return {
        "tenant_id": tenant_id,
        "plugin": plugin_key,
        "enabled": False,
    }
   
async def _get_plugin_row(session: AsyncSession, plugin_key: str) -> Plugin:
    res = await session.execute(select(Plugin).where(Plugin.key == plugin_key))
    plugin = res.scalar_one_or_none()
    if not plugin:
        raise HTTPException(404, f"Unknown plugin: {plugin_key}")
    return plugin


@router.post("/{tenant_id}/plugins/{plugin_key}:install")
async def install_plugin_for_tenant(
    tenant_id: str,
    plugin_key: str,
    session: AsyncSession = Depends(get_session),
):
    manifest = get_manifest(plugin_key)
    if not manifest:
        raise HTTPException(404, f"Manifest not loaded: {plugin_key}")

    plugin = await _get_plugin_row(session, plugin_key)

    try:
        lifecycle = PluginLifecycleManager(session)
        apply_res = await lifecycle.ensure_installed_for_tenant(tenant_id, plugin_key)
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return {
        "tenant_id": tenant_id,
        "plugin": plugin_key,
        "enabled": True,
        "installed": apply_res.installed,
        "upgraded": apply_res.upgraded,
        "from_version": apply_res.from_version,
        "to_version": apply_res.to_version,
    }


@router.post("/{tenant_id}/plugins/{plugin_key}:upgrade")
async def upgrade_plugin_for_tenant(
    tenant_id: str,
    plugin_key: str,
    session: AsyncSession = Depends(get_session),
):
    manifest = get_manifest(plugin_key)
    if not manifest:
        raise HTTPException(404, f"Manifest not loaded: {plugin_key}")

    plugin = await _get_plugin_row(session, plugin_key)

    # must exist (install first)
    res = await session.execute(
        select(TenantPlugin).where(TenantPlugin.tenant_id == tenant_id, TenantPlugin.plugin_id == plugin.id)
    )
    link = res.scalar_one_or_none()
    if not link:
        raise HTTPException(409, "Plugin not installed for this tenant. Call :install first.")
    was_enabled = bool(link.is_enabled)

    try:
        lifecycle = PluginLifecycleManager(session)
        apply_res = await lifecycle.ensure_installed_for_tenant(tenant_id, plugin_key)
        link.is_enabled = was_enabled
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return {
        "tenant_id": tenant_id,
        "plugin": plugin_key,
        "enabled": bool(link.is_enabled),
        "installed": apply_res.installed,
        "upgraded": apply_res.upgraded,
        "from_version": apply_res.from_version,
        "to_version": apply_res.to_version,
    }
