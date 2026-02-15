from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="floor_plan",
    name="Floor Plan",
    version="0.1.0",
    description="Restaurant zones and table occupancy map.",
    router=router,
    requires=[],
    migrations_path="app.plugins.floor_plan.migrations",
    tables=["floor_plan_zone", "floor_plan_table"],
    seed=seed,
    permissions=["floor_plan.read", "floor_plan.write"],
    ui_pages=[
        {"path": "/floor_plan/zones", "label": "Zones", "icon": "map", "order": 30},
        {"path": "/floor_plan/tables", "label": "Tables", "icon": "grid", "order": 40},
    ],
)

