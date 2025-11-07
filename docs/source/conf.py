

# 1) Tell both autodoc and AutoAPI to mock this module
autodoc_mock_imports = [
    # keep any existing mocks...
    "ndif_ray",
    "ndif_ray.ndif_ray_types", #doesn't need autodoc, in ignore list, mock for fix import err
]
autoapi_python_mock_imports = list(autodoc_mock_imports)

import os, sys, types

# 2) Ensure mocked submodules exist and are attached to their parents
def _ensure_mock_tree(modname: str):
    parts = modname.split(".")
    parent = None
    for i in range(1, len(parts) + 1):
        name = ".".join(parts[:i])
        mod = sys.modules.get(name)
        if mod is None:
            mod = types.ModuleType(name)
            sys.modules[name] = mod
        if parent is not None:
            setattr(parent, parts[i-1], mod)  # enables "from parent import child"
        parent = mod
        
for name in autodoc_mock_imports:
    _ensure_mock_tree(name)
    
# Attach the constants now (so import-time access won't fail)
mock = sys.modules["ndif_ray.ndif_ray_types"]
setattr(mock, "MODEL_KEY", "MODEL_KEY")
setattr(mock, "RAY_APP_NAME", "RAY_APP_NAME")
setattr(mock, "NODE_ID", "NODE_ID")

# Tell Sphinx/AutoAPI to mock this module too (belt-and-suspenders)
autodoc_mock_imports = ["ndif_ray.ndif_ray_types"]
autoapi_python_mock_imports = list(autodoc_mock_imports)
    
print("[CONF] mocked?", "ndif_ray.ndif_ray_types" in sys.modules)
print("[CONF] MODEL_KEY preset?", getattr(sys.modules.get("ndif_ray.ndif_ray_types"), "MODEL_KEY", None))

'''
#If controller.py reads those constants at import-time, attach dummies to the mock:
#so attribute access won's fail
m = sys.modules.get("ndif_ray.ndif_ray_types")
if m is not None:
    setattr(m, "MODEL_KEY", "MODEL_KEY")
    setattr(m, "RAY_APP_NAME", "RAY_APP_NAME")
    setattr(m, "NODE_ID", "NODE_ID")
'''
    

extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

autoapi_keep_files = True


PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
PKG_PARENT   = os.path.join(PROJECT_ROOT, "src", "services", "ray", "src")
sys.path.insert(0, PKG_PARENT)

autoapi_type = "python"
autoapi_dirs = [os.path.join(PKG_PARENT, "ndif_ray")]   # scan full package
autoapi_root = "reference/api"

autoapi_include = [
    "*/ndif_ray/nn/*",
    "*/ndif_ray/deployments/*",
    "*/ndif_ray/distributed/*",
    "*/ndif_ray/resources.py",
]

autoapi_ignore = [
    # exclude whole subpackages
    "*/ndif_ray/metrics/*",
    "*/ndif_ray/config/*",
    "*/ndif_ray/ndif_logging/*",
    "*/ndif_ray/providers/*",
    "*/ndif_ray/schema/*",
    # exclude single file modules
    "*/ndif_ray/ndif_ray_types.py",
]

#temp print
print("[CONF] autoapi_dirs =", autoapi_dirs)
print("[CONF] autoapi_include =", globals().get("autoapi_include"))
print("[CONF] autoapi_ignore =", globals().get("autoapi_ignore"))
