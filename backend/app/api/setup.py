from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import List, Literal, Optional

import anyio
from alembic import command
from alembic.config import Config
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config.settings import settings
from app.core.db.base import Base
from app.core.db.session import get_session
from app.core.plugins.lifecycle import PluginLifecycleManager
from app.core.plugins.models import Plugin
from app.core.plugins.registry import list_manifests, validate_enabled_dependencies
from app.core.security.models import User
from app.core.security.utils import get_password_hash
from app.core.tenancy.models import Tenant

router = APIRouter(prefix="/setup", tags=["setup"])

BACKEND_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SQLITE_FILE = "data.db"


class SetupStatus(BaseModel):
    is_setup: bool
    is_initialized: bool  # Alias for is_setup for clarity


class PluginItem(BaseModel):
    key: str
    name: str
    description: str
    version: str
    requires: Optional[List[str]] = None


class SetupRequest(BaseModel):
    tenant_name: str
    tenant_slug: str
    currency: str = "USD"
    locale: str = "en"

    admin_username: str
    admin_password: str
    admin_name: str

    enabled_plugins: List[str] = Field(default_factory=list)


class SetupDatabaseConfig(BaseModel):
    kind: Literal["sqlite", "postgres"] = "sqlite"
    sqlite_path: str = DEFAULT_SQLITE_FILE
    postgres_url: Optional[str] = None

    @model_validator(mode="after")
    def validate_kind_options(self):
        if self.kind == "sqlite" and not self.sqlite_path.strip():
            raise ValueError("sqlite_path is required for sqlite mode")
        if self.kind == "postgres" and not (self.postgres_url or "").strip():
            raise ValueError("postgres_url is required for postgres mode")
        return self


class SetupBootstrapRequest(BaseModel):
    db: SetupDatabaseConfig
    setup: SetupRequest


def _normalize_database_url(db: SetupDatabaseConfig) -> str:
    if db.kind == "sqlite":
        sqlite_path = Path(db.sqlite_path.strip() or DEFAULT_SQLITE_FILE)
        if not sqlite_path.is_absolute():
            sqlite_path = (BACKEND_ROOT / sqlite_path).resolve()
        return f"sqlite+aiosqlite:///{sqlite_path.as_posix()}"

    postgres_url = (db.postgres_url or "").strip()
    if postgres_url.startswith("postgres://"):
        postgres_url = "postgresql://" + postgres_url[len("postgres://") :]

    if postgres_url.startswith("postgresql+asyncpg://"):
        return postgres_url
    if postgres_url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + postgres_url[len("postgresql://") :]
    if postgres_url.startswith("postgresql+psycopg://"):
        return "postgresql+asyncpg://" + postgres_url[len("postgresql+psycopg://") :]
    if postgres_url.startswith("postgresql+psycopg2://"):
        return "postgresql+asyncpg://" + postgres_url[len("postgresql+psycopg2://") :]

    raise ValueError("Unsupported postgres URL format")


def _setup_env_path() -> Path:
    override = os.getenv("SETUP_ENV_PATH")
    if override:
        return Path(override)
    return BACKEND_ROOT / ".env"


def _write_database_url_to_env(database_url: str) -> Path:
    env_path = _setup_env_path()
    env_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines()

    updated = False
    for idx, line in enumerate(lines):
        if line.startswith("DATABASE_URL="):
            lines[idx] = f"DATABASE_URL={database_url}"
            updated = True
            break

    if not updated:
        lines.append(f"DATABASE_URL={database_url}")

    env_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return env_path


async def _run_core_migrations(database_url: str) -> None:
    cfg = Config(str(BACKEND_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    cfg.set_main_option("sqlalchemy.url", database_url)

    def can_recover_by_stamping_head(exc: Exception) -> bool:
        # Common case during setup retry on sqlite:
        # schema objects already exist but alembic version table/history is missing.
        message = str(exc).lower()
        return database_url.startswith("sqlite+") and "already exists" in message

    def worker() -> None:
        try:
            command.upgrade(cfg, "head")
        except Exception as exc:
            if can_recover_by_stamping_head(exc):
                command.stamp(cfg, "head")
                return
            raise

    await anyio.to_thread.run_sync(worker)


async def _sync_plugins_table(session: AsyncSession) -> None:
    for manifest in list_manifests():
        plugin = (
            await session.execute(select(Plugin).where(Plugin.key == manifest.key))
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
    await session.flush()


async def _apply_setup_to_session(
    data: SetupRequest, session: AsyncSession, *, database_url: str
) -> dict:
    try:
        # 1. Verify not already setup
        count = (await session.execute(select(func.count()).select_from(User))).scalar()
        if count > 0:
            raise HTTPException(status_code=400, detail="Application already set up")

        # 2. Validate tenant slug uniqueness
        existing_tenant = (
            await session.execute(select(Tenant).where(Tenant.slug == data.tenant_slug))
        ).scalar_one_or_none()
        if existing_tenant:
            raise HTTPException(status_code=400, detail="Tenant slug already exists")

        # 3. Validate plugins
        all_manifests = list_manifests(sorted_=True)
        all_manifest_keys = {m.key for m in all_manifests}
        unknown_plugins = sorted(set(data.enabled_plugins) - all_manifest_keys)
        if unknown_plugins:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "unknown_plugins",
                    "plugins": unknown_plugins,
                },
            )

        try:
            validate_enabled_dependencies(data.enabled_plugins, all_manifests)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        # 4. Ensure plugins table exists and is synchronized.
        await _sync_plugins_table(session)
        await session.commit()

        tenant_id = str(uuid.uuid4())

        # 5. Install + enable plugins (migrations + seed + installed_version)
        # Run before tenant/user insert to avoid sqlite lock with concurrent DDL.
        if data.enabled_plugins:
            found_keys = set(
                (
                    await session.execute(
                        select(Plugin.key).where(Plugin.key.in_(data.enabled_plugins))
                    )
                ).scalars().all()
            )
            missing_in_db = sorted(set(data.enabled_plugins) - found_keys)
            if missing_in_db:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "plugins_missing_in_db",
                        "plugins": missing_in_db,
                        "hint": "Ensure plugin loader/runtime sync has run before setup.",
                    },
                )

            enabled_set = set(data.enabled_plugins)
            ordered_enabled = [m.key for m in all_manifests if m.key in enabled_set]
            await session.commit()

            lifecycle = PluginLifecycleManager(session, database_url=database_url)
            for plugin_key in ordered_enabled:
                await lifecycle.ensure_installed_for_tenant(tenant_id, plugin_key)
                await session.commit()

        # 6. Create tenant + admin user
        tenant = Tenant(
            id=tenant_id,
            name=data.tenant_name,
            slug=data.tenant_slug,
            currency=data.currency,
            locale=data.locale,
        )
        session.add(tenant)

        hashed_pw = get_password_hash(data.admin_password)
        user = User(
            username=data.admin_username,
            hashed_password=hashed_pw,
            full_name=data.admin_name,
            is_superuser=True,
            tenant_id=tenant_id,
            is_active=True,
        )
        session.add(user)

        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return {"message": "Setup completed successfully", "tenant_id": tenant.id}


@router.get("/status", response_model=SetupStatus)
async def get_setup_status(session: AsyncSession = Depends(get_session)):
    """Check if the application has been set up (any user exists)."""
    count = (await session.execute(select(func.count()).select_from(User))).scalar()
    is_setup = count > 0
    return {"is_setup": is_setup, "is_initialized": is_setup}


@router.get("/plugins", response_model=List[PluginItem])
async def list_available_plugins():
    """List all available plugins for selection during setup."""
    manifests = list_manifests(sorted_=True)
    return [
        PluginItem(
            key=m.key,
            name=m.name,
            description=m.description,
            version=m.version,
            requires=m.requires,
        )
        for m in manifests
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
async def setup_instance(
    data: SetupRequest, session: AsyncSession = Depends(get_session)
):
    return await _apply_setup_to_session(
        data, session, database_url=settings.database_url
    )


@router.post("/bootstrap", status_code=status.HTTP_201_CREATED)
async def bootstrap_instance(data: SetupBootstrapRequest):
    try:
        database_url = _normalize_database_url(data.db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        env_path = _write_database_url_to_env(database_url)
        await _run_core_migrations(database_url)

        engine = create_async_engine(database_url, echo=False)
        session_maker = async_sessionmaker(engine, expire_on_commit=False)
        try:
            # Some environments still rely on metadata create_all for core tables
            # not yet represented in Alembic revisions.
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            async with session_maker() as session:
                result = await _apply_setup_to_session(
                    data.setup, session, database_url=database_url
                )
        finally:
            await engine.dispose()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "setup_bootstrap_failed",
                "message": str(exc),
            },
        ) from exc

    return {
        **result,
        "config_path": str(env_path),
        "restart_required": (database_url != settings.database_url),
    }
