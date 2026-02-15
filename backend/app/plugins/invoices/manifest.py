from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="invoices",
    name="Invoices",
    version="0.1.0",
    description="Legal invoices generated from customer account data.",
    router=router,
    requires=["customers"],
    migrations_path="app.plugins.invoices.migrations",
    tables=["invoice"],
    seed=seed,
    permissions=["invoices.read", "invoices.write"],
    ui_pages=[
        {"path": "/invoices/list", "label": "Invoices", "icon": "file-text", "order": 90},
    ],
)
