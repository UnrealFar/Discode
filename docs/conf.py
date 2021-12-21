# Config file for docs

import re
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("extensions"))

project = "DisCode"

copyright = "2021-present TheFarGG"
author = "TheFarGG"

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', open("../discode/__init__.py").read(), re.MULTILINE).group(1)

release = version if version else "Unknown"

branch = "master" if version.endswith("a") else "v" + release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon"
]

autodoc_member_order = "bysource"
autodoc_typehints = "none"
autodoc_inherit_docstrings = False

master_doc = "index"

extlinks = {
    "github": ("https://github.com/TheFarGG/Discode/", "Link to Github Repository")
}

intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None)
}

templates_path = ['_templates']
default_role = "object"
language = None

pygments_style = "friendly"
exclude_patterns = []

htmlhelp_basename = "discode.doc"
html_context = {"dsc": "https://discord.gg/5JXT6npG4X"}
html_show_sphinx = False
html_theme = "furo"
html_static_path = ['_static']