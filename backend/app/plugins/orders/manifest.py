from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="orders",
    name="Orders",
    version="0.1.0",
    description="Order and order line workflow.",
    router=router,
    requires=["catalog_product"],
    migrations_path="app.plugins.orders.migrations",
    tables=["orders", "order_line"],
    seed=seed,
    permissions=["orders.read", "orders.write"],
    ui_pages=[
        {"path": "/orders/list", "label": "Commandes", "icon": "receipt", "order": 50},
    ],
)
