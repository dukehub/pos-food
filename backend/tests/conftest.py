import os
import importlib
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    # DB sqlite de test isolée au niveau session
    tmpdir = tmp_path_factory.mktemp("db_core")
    db_path = tmpdir / "test_core.db"
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path}"

    # Recharger les modules qui encapsulent settings/engine/dependencies
    import app.core.config.settings as settings_mod
    importlib.reload(settings_mod)

    import app.core.db.session as session_mod
    importlib.reload(session_mod)

    import app.core.plugins.runtime as plugins_runtime_core
    importlib.reload(plugins_runtime_core)

    import app.api.plugins_runtime as plugins_runtime_api
    importlib.reload(plugins_runtime_api)

    import app.main as main_mod
    importlib.reload(main_mod)

    with TestClient(main_mod.app) as c:
        yield c
