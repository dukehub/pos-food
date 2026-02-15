from app.core.plugins.manifest import PluginManifest
from app.core.plugins.registry import (
    PluginManifestConflictError,
    clear_manifests,
    register_manifest,
)


def test_register_manifest_rejects_duplicate_key_with_different_manifest():
    clear_manifests()
    first = PluginManifest(key="dup", name="A", version="1.0.0")
    second = PluginManifest(key="dup", name="B", version="1.0.1")

    register_manifest(first)

    try:
        register_manifest(second)
        assert False, "Expected PluginManifestConflictError for duplicate key"
    except PluginManifestConflictError:
        pass
    finally:
        clear_manifests()
