# templtest -- a tool for testing Ansible role templates
# Copyright (C) 2021  Alexey Busygin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
from unittest import TestCase

try:
    # pylint: disable=unused-import
    # Mypy type checking is currently disabled. See issue #1153.
    from importlib.resources import path as resource_path   # type: ignore
except ImportError:
    # pylint: disable=unused-import
    # Mypy type checking is currently disabled. See issue #1153.
    from importlib_resources import path as resource_path   # type: ignore

from ..util import (
    extract_role,
    TempDirectory,
)


class ExtractRole(TestCase):

    def test(self):
        with TempDirectory() as tmpdir_path:
            extract_role("without_variable_definition", tmpdir_path)
            actual = sorted(tmpdir_path.glob("**/*"))
            expect = [
                Path(tmpdir_path, "without_variable_definition"),
                Path(tmpdir_path, "without_variable_definition",
                     "templates"),
                Path(tmpdir_path, "without_variable_definition",
                     "templates", "foo.j2"),
                Path(tmpdir_path, "without_variable_definition",
                     "templates_tests"),
                Path(tmpdir_path, "without_variable_definition",
                     "templates_tests", "foo"),
                Path(tmpdir_path, "without_variable_definition",
                     "templates_tests", "meta.yml"),
                Path(tmpdir_path, "without_variable_definition",
                     "templates_tests", "test.yml"),
            ]
            self. assertEqual(expect, actual)

            template_path = Path(tmpdir_path, "without_variable_definition",
                                 "templates", "foo.j2")
            actual = template_path.read_text(encoding="utf-8")
            expect = "{{ foo|default(\"\") }}\n"
            self.assertEqual(expect, actual)

    def test_not_found(self):
        with TempDirectory() as tmpdir_path:
            with self.assertRaises(KeyError) as ctxmgr:
                extract_role("not_exists", tmpdir_path)
            actual = ("role 'not_exists' meta is not found",)
            expect = ctxmgr.exception.args
            self.assertEqual(expect, actual)
