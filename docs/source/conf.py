import os
import sys
from datetime import date
#added
import types

# Belt-and-suspenders: make sure mocked modules exist AND are attributes of parents.
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
            setattr(parent, parts[i-1], mod)  # expose child on parent for "from parent import child"
        parent = mod

def _ensure_mock(modname):
    if modname in sys.modules:
        return sys.modules[modname]
    module = types.ModuleType(modname)
    sys.modules[modname] = module
    return module


# ---------------------------------------------------------
# Project metadata
# ---------------------------------------------------------
project = "NDIF Ray – nn API"
author = "NDIF Team"
copyright = f"{date.today().year}, {author}"

#sys.path points to the top-level
#sys.path.insert(0, os.path.abspath("../../src"))
# 1) Put the *package parent* of ndif_ray on sys.path so imports are ndif_ray.*
#    (…/src/services/ray/src)
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
PKG_PARENT   = os.path.join(PROJECT_ROOT, "src", "services", "ray", "src")
sys.path.insert(0, PKG_PARENT)

# ---------------------------------------------------------
# Sphinx extensions
# ---------------------------------------------------------
extensions = [
    "myst_parser",             # Markdown pages (optional but handy)
    "sphinx.ext.napoleon",     # Google/Numpy-style docstrings
    #"sphinx.ext.autosectionlabel",
    "autoapi.extension",       # <-- AutoAPI for source parsing
]

# Recognize both .rst and .md (optional)
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Theme
html_theme = "furo"

# ---------------------------------------------------------
# Path setup (not strictly needed for AutoAPI since it parses
# source files directly, but safe to keep for future)
# ---------------------------------------------------------
# repo_root = <docs/source>/../../
#repo_root = os.path.abspath(os.path.join(__file__, "..", ".."))
repo_root = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
# code_root = <repo_root>/src/services/ray/src
code_root = os.path.join(repo_root, "src", "services", "ray", "src")
# If you later add manual autodoc pages (not AutoAPI), uncomment:
# sys.path.insert(0, code_root)

# ---------------------------------------------------------
# AutoAPI configuration – scope ONLY to ndif_ray/nn
# ---------------------------------------------------------
autoapi_type = "python"
#autoapi_dirs = [os.path.join(code_root, "ndif_ray", "nn")]  # <-- target
#autoapi_dirs = [os.path.abspath("../../src")] 
#autoapi_dirs = [PKG_PARENT]

autoapi_dirs = [os.path.join(PKG_PARENT, "ndif_ray")]


#autoapi_root = "reference/api/ndif_ray/nn"                  # where pages land (under docs/source)
autoapi_root = "reference/api"
# Optional filters
autoapi_file_patterns = ["*.py", "**/*.py"]
autoapi_ignore = ["**/tests/**", "**/__init__.py"]  # adjust as you like
autoapi_keep_files = True  # keep generated .rst (useful to inspect diffs)

autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    # "imported-members",  # enable if you re-export many symbols
    "special-members",     # e.g., __call__
]

# ---------------------------------------------------------
# If your type hints or docs reference heavy deps, mock them
# (AutoAPI doesn't import, but cross-refs or templates can)
# ---------------------------------------------------------
autodoc_mock_imports = [
    "torch",
    "numpy",
    # Add others if needed
    "ray",
    "ray.serve",
    "ray.dashboard",
    "ray.dashboard.modules",
    "ray.dashboard.modules.serve",
    "ray.dashboard.modules.serve.sdk",
]

for name in autodoc_mock_imports:
    _ensure_mock_tree(name)
    

for name in autodoc_mock_imports:
    # Create parent packages first: "ray.dashboard.modules.serve.sdk"
    parts = name.split(".")
    for i in range(1, len(parts)+1):
        _ensure_mock(".".join(parts[:i]))
        


# AutoAPI also respects this in recent versions
autoapi_python_mock_imports = list(autodoc_mock_imports)

# ---------------------------------------------------------
# Sphinx basics
# ---------------------------------------------------------
master_doc = "index"
html_permalinks_icon = "§"

#added
autoapi_python_use_implicit_namespaces = True

#temporary workaround for persistent error of Cannot resolve import of unknown module 
# ndif_ray.providers in ndif_ray.providers.raytelling AutoAPI to skip this module
autoapi_ignore = [
    "*/ndif_ray/providers/ray.py",
]


#for debugging
print("[CONF] PROJECT_ROOT =", PROJECT_ROOT)
print("[CONF] PKG_PARENT   =", PKG_PARENT)
print("[CONF] autoapi_dirs =", autoapi_dirs)
print("[CONF] sys.path[0]  =", sys.path[0])

