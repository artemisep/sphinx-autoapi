from importlib import import_module as _im
__all__ = ["protected_environment", "protected_objects"]
for _n in list(__all__):
    try: globals()[_n] = _im(f"{__name__}.{_n}")
    except Exception: pass
