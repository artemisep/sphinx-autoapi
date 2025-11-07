from importlib import import_module as _im
__all__ = ["base", "model", "util"]
for _n in list(__all__):
    try: globals()[_n] = _im(f"{__name__}.{_n}")
    except Exception: pass
