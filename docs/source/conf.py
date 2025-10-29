import os
import sys
from datetime import date

# ---- Project metadata ----
project = "NDIF Ray NN API"
author = "NDIF Team"
copyright = f"{date.today().year}, NDIF"

# ---- General Sphinx config ----
extensions = [
    "myst_parser",            # optional if you keep everything in .rst
    "sphinx.ext.napoleon",    # Google/Numpy docstrings, if you use them
    "sphinx.ext.autosectionlabel",
    "autoapi.extension",      # <-- the key extension
]

# You can keep source_suffix default; adding .md if you want Markdown landing pages:
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Theme
html_theme = "furo"

# If you *haven't* renamed the top-level "logging" dir yet, protect stdlib imports:
# Force stdlib logging to resolve before local "logging/"
# (Best fix is still renaming your "logging" dir.)
import logging  # noqa: F401

# ---- AutoAPI: scope to just ray/nn ----
# IMPORTANT: AutoAPI parses source; it does *not* import your package.
# Point it at the directory that directly contains the modules you want documented.
repo_root = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
code_root = os.path.join(repo_root, "src", "services", "ray", "src")

autoapi_type = "python"
autoapi_dirs = [os.path.join(code_root, "ray", "nn")]    # <-- only nn

# Where generated .rst files will be placed *inside* docs/source
autoapi_root = "reference/api/services/ray/nn"

# Optional: limit files inside nn (keeps things explicit)
autoapi_python_use_implicit_namespaces = True
autoapi_file_patterns = ["*.py", "**/*.py"]
autoapi_ignore = ["**/tests/**", "**/__init__.py"]   # tune to taste

# Useful display options
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",        # shows __call__, etc.
    "imported-members",       # only if you want re-exported items; can be noisy
]

# If any modules try to import heavy/absent deps in annotations, add them here to silence:
# (AutoAPI doesn’t import, but some templates/intersphinx cross-refs might)
autodoc_mock_imports = [
    "ray",          # real Ray if it’s not installed (only needed if cross-refs)
    "torch",
    "numpy",
]

# Keep generated files to debug what AutoAPI produced (optional)
autoapi_keep_files = True

# Master docs
master_doc = "index"

# Clean, short URLs (optional)
html_permalinks_icon = "§"
