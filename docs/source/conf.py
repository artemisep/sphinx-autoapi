import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
PKG_PARENT   = os.path.join(PROJECT_ROOT, "src", "services", "ray", "src")
sys.path.insert(0, PKG_PARENT)

extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

autoapi_type = "python"
autoapi_dirs = [os.path.join(PKG_PARENT, "ndif_ray")]  # scan the package folder itself
autoapi_root = "reference/api"

autoapi_keep_files = True


PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
PKG_PARENT   = os.path.join(PROJECT_ROOT, "src", "services", "ray", "src")
sys.path.insert(0, PKG_PARENT)

autoapi_type = "python"
autoapi_dirs = [os.path.join(PKG_PARENT, "ndif_ray")]   # scan full package
autoapi_root = "reference/api"

autoapi_ignore = [
    # exclude whole subpackages
    "*/ndif_ray/metrics/*",
    "*/ndif_ray/config/*",
    "*/ndif_ray/ndif_logging/*",
    "*/ndif_ray/providers/*",
    # exclude single file modules
    "*/ndif_ray/ndif_ray_types.py",
]

