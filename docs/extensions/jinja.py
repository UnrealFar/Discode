r"""
An ext to use Jinja in our docs.

SOURCE:
https://github.com/Mecha-Karen/acord
"""

from sphinx.application import Sphinx

import discode


def worker(app: Sphinx, docname: str, source: list):
    if app.builder.format != "html":
        return

    src = source[0]
    rendered_source = app.builder.templates.render_string(
        src,
        {
            "discode": discode,
            "getattr": getattr,
            "dir": dir,
            "disallow": [
                "Messageable",
            ],
            "allowed_enums": [
                "ButtonStyle",
            ],
            "LINE_SEP": "\n",
        },
    )

    source[0] = rendered_source


def setup(app: Sphinx):
    app.connect("source-read", worker)
