from app.core.plugins.manifest import PluginManifest
from .router import router
from .seed import seed

manifest = PluginManifest(
    key="catalog_product_i18n",
    name="Catalog Product i18n",
    version="0.1.0",
    description="Product catalog management + i18n.",
    router=router,
    requires=["catalog_product"],
    migrations_path="app.plugins.catalog_product_i18n.migrations",
    tables=["categories", "products"],  # optionnel mais utile
    seed=seed,
    permissions=["catalog_product_i18n.read", "catalog_product_i18n.write"],
    ui_pages=[
        {"path": "/catalog_product_i18n/products", "label": "Produits", "icon": "box", "order": 10},
        {"path": "/catalog_product_i18n/categories", "label": "Catégories", "icon": "tag", "order": 20},
    ],
)