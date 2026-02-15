from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="kds",
    name="KDS",
    version="0.1.0",
    description="Kitchen display screen setup and connectivity.",
    router=router,
    requires=["devices"],
    migrations_path="app.plugins.kds.migrations",
    tables=["device_kds"],
    seed=seed,
    permissions=["kds.read", "kds.write"],
    ui_pages=[
        {"path": "/kds/kds", "label": "KDS", "icon": "monitor-smartphone", "order": 81},
    ],
)
