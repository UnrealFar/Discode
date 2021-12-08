# Config file for docs

import re
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Discode"

copyright = "Copyright (c) 2021-present TheFarGG"
author = "TheFarGG"

version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', open("../discode/__init__.py").read(), re.MULTILINE).group(1)

release = version

branch = "master" if release.endswith("a") else "v" + release

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
    "github": ("https://github.com/TheFarGG/Discode/%s", "Link to Github Repository")
}

templates_path = ['_templates']

language = 'en'

exclude_patterns = []

html_show_sphinx = False
html_theme = "groundwork"

html_static_path = ['_static']