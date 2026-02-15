from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="printer",
    name="Printer",
    version="0.1.0",
    description="Printer connectivity and setup.",
    router=router,
    requires=["devices"],
    migrations_path="app.plugins.printer.migrations",
    tables=["device_printer"],
    seed=seed,
    permissions=["printer.read", "printer.write"],
    ui_pages=[
        {"path": "/printer/printers", "label": "Imprimantes", "icon": "printer", "order": 80},
    ],
)

