import importlib
import json
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.formatters.html import HtmlFormatter
from django.utils.safestring import mark_safe

from pathlib import Path

GLOBAL_OPTIONS_FILE_PATH = f"{Path.cwd()}/modules/options.json"


def get_options(module_slug, option_key):
    with open(GLOBAL_OPTIONS_FILE_PATH, "r") as f:
        module_options = json.loads(f.read())

    option_value = [
        module.get(option_key)
        for module in module_options["module_options"]
        if module.get("slug") == module_slug
    ]

    default_value = getattr(
        importlib.import_module(f"modules.{module_slug}.options"), option_key
    )

    return option_value[0] if option_value else default_value


def json_style_prettify(data):
    response = json.dumps(data, sort_keys=True, indent=2)
    formatter = HtmlFormatter(style='colorful')
    response = highlight(response, JsonLexer(), formatter)
    style = "<style>" + formatter.get_style_defs() + "</style>"
    return mark_safe(style + response)
