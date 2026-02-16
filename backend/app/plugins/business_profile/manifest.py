from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="business_profile",
    name="Business Profile",
    version="0.1.0",
    description="Restaurant identity, branding, location, and fiscal settings.",
    router=router,
    requires=[],
    migrations_path="app.plugins.business_profile.migrations",
    tables=["restaurant_config"],
    seed=seed,
    permissions=["business_profile.read", "business_profile.write"],
    ui_pages=[],
)

