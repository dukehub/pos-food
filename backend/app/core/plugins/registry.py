# app/core/plugins/registry.py
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from app.core.plugins.manifest import PluginManifest


# ---------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------

class PluginDependencyError(RuntimeError):
    pass


class PluginDependencyCycleError(RuntimeError):
    pass


class PluginManifestConflictError(RuntimeError):
    pass


# ---------------------------------------------------------------------
# Dependency utils (topological sort + enabled validation)
# ---------------------------------------------------------------------

def sort_manifests_topologically(manifests: Iterable[PluginManifest]) -> List[PluginManifest]:
    manifests = list(manifests)
    by_key: Dict[str, PluginManifest] = {m.key: m for m in manifests}

    # Missing deps
    missing: List[Tuple[str, str]] = []
    for m in manifests:
        for dep in (m.requires or []):
            if dep not in by_key:
                missing.append((m.key, dep))
    if missing:
        details = ", ".join([f"{k} -> {dep}" for k, dep in missing])
        raise PluginDependencyError(f"Missing plugin dependencies: {details}")

    # Kahn topo sort
    in_degree: Dict[str, int] = {m.key: 0 for m in manifests}
    dependents: Dict[str, List[str]] = {m.key: [] for m in manifests}

    for m in manifests:
        deps = m.requires or []
        in_degree[m.key] = len(deps)
        for dep in deps:
            dependents[dep].append(m.key)

    queue: List[str] = [k for k, deg in in_degree.items() if deg == 0]

    ordered_keys: List[str] = []
    while queue:
        k = queue.pop(0)
        ordered_keys.append(k)

        for child in dependents[k]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    if len(ordered_keys) != len(manifests):
        cyclic = [k for k, deg in in_degree.items() if deg > 0]
        raise PluginDependencyCycleError(f"Cycle detected in plugin dependencies: {cyclic}")

    return [by_key[k] for k in ordered_keys]


def validate_enabled_dependencies(
    enabled_keys: Iterable[str],
    manifests: Iterable[PluginManifest],
) -> None:
    enabled = set(enabled_keys)
    by_key: Dict[str, PluginManifest] = {m.key: m for m in manifests}

    missing: List[Tuple[str, str]] = []
    for k in enabled:
        m = by_key.get(k)
        if not m:
            continue
        for dep in (m.requires or []):
            if dep not in enabled:
                missing.append((k, dep))

    if missing:
        details = ", ".join([f"{k} requires {dep}" for k, dep in missing])
        raise PluginDependencyError(f"Enabled plugins missing required deps: {details}")


# ---------------------------------------------------------------------
# Manifest registry (used by loader/bootstrap/runtime)
# ---------------------------------------------------------------------

_MANIFESTS: Dict[str, PluginManifest] = {}


def register_manifest(manifest: PluginManifest) -> None:
    """
    Called by AsyncPluginLoader.
    Rejects duplicate keys with a different manifest object to avoid silent override.
    """
    existing = _MANIFESTS.get(manifest.key)
    if existing is not None and existing is not manifest:
        raise PluginManifestConflictError(
            f"Duplicate plugin manifest key detected: {manifest.key}"
        )
    _MANIFESTS[manifest.key] = manifest


def list_manifests(*, sorted_: bool = True) -> List[PluginManifest]:
    """
    Used by bootstrap.py/runtime.py to iterate plugins.
    sorted_=True ensures dependency order (requires first).
    """
    manifests = list(_MANIFESTS.values())
    if not sorted_:
        return manifests
    return sort_manifests_topologically(manifests)


def get_manifest(key: str) -> PluginManifest | None:
    return _MANIFESTS.get(key)


def clear_manifests() -> None:
    _MANIFESTS.clear()
