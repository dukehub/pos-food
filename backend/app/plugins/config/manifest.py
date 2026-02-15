from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="config",
    name="Configuration",
    version="0.1.0",
    description="Restaurant identity, branding, location, and fiscal settings.",
    router=router,
    requires=[],
    migrations_path="app.plugins.config.migrations",
    tables=["restaurant_config"],
    seed=seed,
    permissions=["config.read", "config.write"],
    ui_pages=[],
)

