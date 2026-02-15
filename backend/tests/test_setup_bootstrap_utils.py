import os

from app.api.setup import (
    SetupDatabaseConfig,
    _normalize_database_url,
    _write_database_url_to_env,
)


def test_normalize_sqlite_url_uses_async_driver():
    db = SetupDatabaseConfig(kind="sqlite", sqlite_path="data_test.db")
    url = _normalize_database_url(db)
    assert url.startswith("sqlite+aiosqlite:///")
    assert url.endswith("/backend/data_test.db")


def test_normalize_postgres_url_promotes_async_driver():
    db = SetupDatabaseConfig(
        kind="postgres",
        postgres_url="postgresql://user:pass@localhost:5432/restaurant_pos",
    )
    url = _normalize_database_url(db)
    assert url == "postgresql+asyncpg://user:pass@localhost:5432/restaurant_pos"


def test_write_database_url_to_env_updates_file(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("APP_NAME=restaurant-pos\nDATABASE_URL=sqlite+aiosqlite:///old.db\n")
    os.environ["SETUP_ENV_PATH"] = str(env_path)
    try:
        written_path = _write_database_url_to_env("sqlite+aiosqlite:///new.db")
    finally:
        del os.environ["SETUP_ENV_PATH"]

    content = written_path.read_text(encoding="utf-8")
    assert "APP_NAME=restaurant-pos" in content
    assert "DATABASE_URL=sqlite+aiosqlite:///new.db" in content
