from dataclasses import dataclass
from typing import Any, Callable, Optional

from fastapi import APIRouter

SeedFn = Callable[[Any, str], "awaitable[None]"]  # (session, tenant_id)

@dataclass(frozen=True)
class PluginManifest:
    key: str
    name: str
    version: str
    description: str = ""
    router: Optional[APIRouter] = None
    requires: Optional[list[str]] = None
# --- NEW: lifecycle / migrations / UI ---
    migrations_path: Optional[str] = None  # ex: "app.plugins.catalog_product.migrations"
    tables: Optional[list[str]] = None      # tables gérées par ce plugin
    seed: Optional[SeedFn] = None           # données initiales + permissions
    permissions: Optional[list[str]] = None # ex: ["catalog.read", "catalog.write"]
    ui_pages: Optional[list[dict]] = None   # ex: [{"path":"/catalog/products", "label":"Produits", ...}]