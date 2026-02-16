from app.core.plugins.manifest import PluginManifest
from app.plugins.app_settings.router import router
from app.plugins.app_settings.seed import seed


manifest = PluginManifest(
    key="config",
    name="App Settings",
    version="0.1.0",
    description="Global tenant configuration and settings registry.",
    router=router,
    requires=[],
    migrations_path="app.plugins.app_settings.migrations",
    seed=seed,
    permissions=["app_settings.read", "app_settings.write"],
    ui_pages=[{"path": "/settings", "label": "Settings", "icon": "settings", "order": 10}],
)
