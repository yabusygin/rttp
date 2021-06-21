from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader
from yaml import safe_load


TemplateVars = Dict[str, Any]


class TemplateRenderer:

    _DEFAULT_FILENAMES = ["main.yml", "main.yaml", "main"]

    def __init__(self, role: Path):
        self._role = role
        self._environment = Environment(
            loader=FileSystemLoader(
                searchpath=str(Path(self._role, "templates")),
            ),
            keep_trailing_newline=True,
            lstrip_blocks=True,
            trim_blocks=True,
        )

    def render(self,
               template: Path,
               inventory: Path = None,
               extra: Path = None) -> str:
        renderer = self._environment.get_template(str(template))
        inventory_variables = _load_variables(inventory) \
            if inventory is not None \
            else None
        extra_variables = _load_variables(extra) \
            if extra is not None \
            else None
        variables = self._merge_variables(inventory_variables, extra_variables)
        return renderer.render(**variables)

    def _merge_variables(self,
                         inventory: TemplateVars = None,
                         extra: TemplateVars = None) -> TemplateVars:
        if inventory is None:
            inventory = {}
        if extra is None:
            extra = {}

        result = {}
        result.update(self._load_role_variables(dirname="defaults"))
        result.update(inventory)
        result.update(self._load_role_variables(dirname="vars"))
        result.update(extra)
        return result

    def _load_role_variables(self, dirname: str) -> TemplateVars:
        for filename in self._DEFAULT_FILENAMES:
            path = Path(self._role, dirname, filename)
            if not path.is_file():
                continue
            return _load_variables(path)
        return {}


def _load_variables(path: Path) -> TemplateVars:
    data = path.read_text()
    return safe_load(data)
