import os
import sys
import importlib
import pkgutil

# Set path to backend root
sys.path.insert(0, os.getcwd())

def check_imports():
    print("Checking imports...")
    try:
        import app.core.db.base
        print("Core DB Base imported.")
    except Exception as e:
        print(f"Failed to import core db base: {e}")
        return

    import app.plugins
    for finder, name, ispkg in pkgutil.iter_modules(app.plugins.__path__):
        if name.startswith("_"):
            continue
        try:
            print(f"Importing app.plugins.{name}.models...")
            importlib.import_module(f"app.plugins.{name}.models")
            print(f"OK: app.plugins.{name}.models")
        except ImportError as e:
            print(f"FAILED (ImportError): app.plugins.{name}.models - {e}")
        except NameError as e:
            print(f"FAILED (NameError): app.plugins.{name}.models - {e}")
        except Exception as e:
            print(f"FAILED (Exception): app.plugins.{name}.models - {e}")

if __name__ == "__main__":
    check_imports()
