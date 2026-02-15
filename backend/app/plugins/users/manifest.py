from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="users",
    name="Users",
    version="0.1.0",
    description="POS operators, servers, and tenant internal roles.",
    router=router,
    requires=[],
    migrations_path="app.plugins.users.migrations",
    tables=["staff_user"],
    seed=seed,
    permissions=["users.read", "users.write"],
    ui_pages=[
        {"path": "/users/list", "label": "Users", "icon": "user", "order": 70},
    ],
)
