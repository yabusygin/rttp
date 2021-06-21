from difflib import unified_diff
from pathlib import Path
from typing import Optional

from .discovery import TestDefinition, Variables
from .exception import AssertError
from .template import TemplateRenderer


class Test:
    _role_path: Path
    _test_definition_src_path: Path
    _test_definition: TestDefinition
    _renderer: TemplateRenderer

    def __init__(self, role_path: Path, src_path: Path,
                 testdef: TestDefinition):
        self._role_path = role_path
        self._test_definition_src_path = src_path
        self._test_definition = testdef
        self._renderer = TemplateRenderer(self._role_path)

    @property
    def _base_path(self) -> Path:
        parent_path = self._test_definition_src_path.parent
        if parent_path.is_absolute():
            return parent_path
        return self._role_path.joinpath("templates_tests", parent_path)

    @property
    def _inventory_path(self) -> Optional[Path]:
        if not self._test_definition.has_inventory():
            return None
        assert isinstance(self._test_definition.variables, Variables)
        assert isinstance(self._test_definition.variables.inventory, Path)
        return self._base_path.joinpath(
            self._test_definition.variables.inventory,
        )

    @property
    def _extra_path(self) -> Optional[Path]:
        if not self._test_definition.has_extra():
            return None
        assert isinstance(self._test_definition.variables, Variables)
        assert isinstance(self._test_definition.variables.extra, Path)
        return self._base_path.joinpath(self._test_definition.variables.extra)

    def run(self) -> None:
        actual = self._renderer.render(
            template=self._test_definition.template,
            inventory=self._inventory_path,
            extra=self._extra_path,
        )

        expect_path = self._base_path.joinpath(
            self._test_definition.expected_result,
        )
        expect = expect_path.read_text()

        diff = "\n".join(
            unified_diff(
                a=expect.splitlines(),
                b=actual.splitlines(),
                fromfile=str(expect_path.relative_to(self._role_path)),
                tofile="render({})".format(
                    Path("templates", self._test_definition.template),
                ),
                lineterm="",
            ),
        )
        if diff:
            raise AssertError(diff)
