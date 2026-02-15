from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="customers",
    name="Customers",
    version="0.1.0",
    description="Customer profiles, contact details, and account limits.",
    router=router,
    requires=[],
    migrations_path="app.plugins.customers.migrations",
    tables=["customer"],
    seed=seed,
    permissions=["customers.read", "customers.write"],
    ui_pages=[
        {"path": "/customers/list", "label": "Customers", "icon": "users", "order": 60},
    ],
)
