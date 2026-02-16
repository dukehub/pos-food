import os
import sys
import importlib
import pkgutil
from typing import Dict, List, Set

# Set path to backend root
sys.path.insert(0, os.getcwd())

def check_manifests():
    print("Checking manifests and dependencies...")
    
    plugins = {}
    
    import app.plugins
    for finder, name, ispkg in pkgutil.iter_modules(app.plugins.__path__):
        if name.startswith("_"):
            continue
        try:
            mod = importlib.import_module(f"app.plugins.{name}.manifest")
            if hasattr(mod, "manifest"):
                manifest = mod.manifest
                plugins[manifest.key] = manifest
                print(f"Loaded manifest for: {manifest.key} (requires: {manifest.requires})")
            else:
                print(f"WARNING: No 'manifest' object in app.plugins.{name}.manifest")
        except Exception as e:
            print(f"FAILED to load manifest: app.plugins.{name}.manifest - {e}")

    print("\nVerifying dependencies...")
    all_keys = set(plugins.keys())
    
    for key, manifest in plugins.items():
        for req in manifest.requires:
            if req not in all_keys:
                print(f"ERROR: Plugin '{key}' requires '{req}' which is NOT loaded.")
            else:
                print(f"  OK: '{key}' dependency '{req}' found.")

if __name__ == "__main__":
    check_manifests()
