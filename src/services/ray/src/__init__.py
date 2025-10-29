# src/services/ray/src/__init__.py
from importlib import import_module as _im
from importlib.util import find_spec as _find_spec
import types as _types

def _safe_import(modpath: str):
    """
    Try to import modpath; if ANY exception occurs (missing optional deps,
    runtime side-effects, etc.), return a harmless shim ModuleType so that
    attribute access exists and docs generation can proceed.
    """
    try:
        # If it doesn't even exist on sys.path, don't try to import
        if _find_spec(modpath) is None:
            return None
        return _im(modpath)
    except Exception:
        return _types.ModuleType(modpath)

# Export canonical subpackages first
_names = ["providers", "ray", "metrics", "schema"]

for _name in _names:
    _mod = _safe_import(f"{__name__}.{_name}")
    if _mod is not None:
        globals()[_name] = _mod

__all__ = [n for n in _names if n in globals()]


'''
from importlib import import_module as _im

# Export canonical subpackages first
__all__ = ["providers", "ray", "metrics", "schema"]

for _name in list(__all__):
    try:
        globals()[_name] = _im(f"{__name__}.{_name}")
    except Exception:
        # Keep docs build resilient when optional deps are missing
        pass
'''
