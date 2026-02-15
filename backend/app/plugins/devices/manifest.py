from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="devices",
    name="Devices",
    version="0.1.0",
    description="Device registry and shared hardware metadata.",
    router=router,
    requires=[],
    migrations_path="app.plugins.devices.migrations",
    tables=["device"],
    seed=seed,
    permissions=["devices.read", "devices.write"],
    ui_pages=[
        {"path": "/devices/devices", "label": "Devices", "icon": "cpu", "order": 79},
    ],
)
