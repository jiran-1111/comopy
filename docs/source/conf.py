# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

project = "ComoPy"
copyright = "2024-2025, Microprocessor R&D Center (MPRC), Peking University"
author = "Chun Yang"

# with open("../../_version.py") as f:
# 	code = compile(f.read(), "../../_version.py", "exec")
# loc = {}
# exec(code, loc)

# version = loc["__version__"]
version = "0.1.0"
# release = ''

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []

# Navigation and cross-reference settings
add_module_names = False  # Don't add module names to object descriptions
add_function_parentheses = True  # Add parentheses to function names
show_authors = True  # Show author information
pygments_style = "sphinx"  # Code highlighting style

# Table of contents settings
master_doc = "index"  # The main toctree document
toc_object_entries_show_parents = "hide"  # Control TOC display of parents


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Theme options for navigation
html_theme_options = {
    "navigation_depth": 4,  # Show navigation up to 4 levels deep
    "collapse_navigation": False,  # Keep navigation expanded
    "sticky_navigation": True,  # Keep navigation visible when scrolling
    "includehidden": True,  # Include hidden toctrees in navigation
    "titles_only": False,  # Show full navigation titles
    "prev_next_buttons_location": "bottom",  # Show Previous/Next at bottom
}

# General navigation settings
html_use_index = True  # Enable index generation
html_show_sourcelink = True  # Show "View page source" links
html_show_sphinx = True  # Show "Created using Sphinx" notice

# Navigation with keyboard support
html_context = {
    "display_github": False,  # Don't show GitHub link (can be enabled later)
    "github_user": "",  # GitHub username (if needed)
    "github_repo": "",  # GitHub repository (if needed)
    "github_version": "",  # GitHub branch (if needed)
    "conf_py_path": "/docs/source/",  # Path to conf.py (if needed)
}
