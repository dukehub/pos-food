from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="product_bundle",
    name="Product Bundle",
    version="0.1.0",
    description="Bundle composition between parent and child products.",
    router=router,
    requires=["catalog_product"],
    migrations_path="app.plugins.product_bundle.migrations",
    tables=["product_bundle_item"],
    seed=seed,
    permissions=["product_bundle.read", "product_bundle.write"],
    ui_pages=[
        {"path": "/product_bundle/list", "label": "Bundles", "icon": "package", "order": 110},
    ],
)
