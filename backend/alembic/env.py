import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config.settings import settings
from app.core.db.base import Base
from app.core.plugins import models  # noqa: F401
from app.plugins.catalog_product import models as catalog_models  # noqa: F401
from app.plugins.catalog_product_i18n import models as catalog_i18n_models  # noqa: F401
from app.core.tenancy import models as tenancy_models  # noqa: F401
from app.core.security import models as security_models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

configured_url = config.get_main_option("sqlalchemy.url")
if configured_url and configured_url != "driver://user:pass@localhost/dbname":
    database_url = configured_url
else:
    database_url = settings.database_url

config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
