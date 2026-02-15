import importlib
import pkgutil
from typing import List

from app.core.plugins.manifest import PluginManifest
from app.core.plugins.registry import clear_manifests, register_manifest


class AsyncPluginLoader:
    async def load_all(self) -> List[PluginManifest]:
        manifests: List[PluginManifest] = []
        clear_manifests()
        package = importlib.import_module("app.plugins")
        for module in pkgutil.iter_modules(package.__path__):
            if module.name.startswith("_"):
                continue
            manifest_module = importlib.import_module(
                f"app.plugins.{module.name}.manifest"
            )
            manifest = getattr(manifest_module, "manifest", None)
            if manifest:
                register_manifest(manifest)
                manifests.append(manifest)
        return manifests
