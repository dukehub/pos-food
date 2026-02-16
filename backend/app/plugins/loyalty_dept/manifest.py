from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="loyalty_dept",
    name="Loyalty Dept",
    version="0.1.0",
    description="Manages customer debts and payments.",
    router=router,
    requires=["customers", "orders"],
    migrations_path="app.plugins.loyalty_dept.migrations",
    tables=["customer_ledger", "customer_account"],
    seed=seed,
    permissions=["loyalty_dept.read", "loyalty_dept.write"],
    ui_pages=[
        {"path": "/loyalty_dept/list", "label": "Loyalty Dept", "icon": "users", "order": 60},
    ],
)
