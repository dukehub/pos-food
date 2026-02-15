from app.core.plugins.manifest import PluginManifest
from .router import router
from .seed import seed

manifest = PluginManifest(
    key="catalog_product",
    name="Catalog Product",
    version="0.1.0",
    description="Product catalog management.",
    router=router,
    requires=[],
    migrations_path="app.plugins.catalog_product.migrations",
    tables=["categories", "products"],  # optionnel mais utile
    seed=seed,
    permissions=["catalog_product.read", "catalog_product.write"],
    ui_pages=[
        {"path": "/catalog_product/products", "label": "Produits", "icon": "box", "order": 10},
        {"path": "/catalog_product/categories", "label": "Catégories", "icon": "tag", "order": 20},
    ],
)