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

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from textwrap import dedent
from unittest import TestCase

from templtest.cli import main

from ...util import extract_role, TempDirectory


class RunProgram(TestCase):

    def test_success(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)

            stream = StringIO()
            with redirect_stdout(stream):
                main(argv=["--role-path={}".format(role_path)])
            actual = stream.getvalue()
            expect = dedent(
                """\
                [test.yml] test variable definition in role "defaults/" ... ok
                [test.yml] test variable definition in inventory ... ok
                """,
            )
            self.assertEqual(expect, actual)

    def test_failure(self):
        with TempDirectory() as tmpdir_path:
            role_name = "test_failure"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)

            stream = StringIO()
            with redirect_stdout(stream):
                main(argv=["--role-path={}".format(role_path)])
            actual = stream.getvalue()
            expect = dedent(
                """\
                [test.yml] this test fails ... fail
                --- templates_tests/foo
                +++ render(templates/foo.j2)
                @@ -1 +1 @@
                -baz
                +bar
                """,
            )
            self.assertEqual(expect, actual)

    def test_invalid_test_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "invalid_path_in_test_definition"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)

            stream = StringIO()
            with redirect_stdout(stream):
                main(argv=["--role-path={}".format(role_path)])
            actual = stream.getvalue()
            expect = ": ".join([
                "TestDefinitionError",
                "invalid definition file 'test.yml'",
                "invalid test definition #0",
                "invalid variables attribute",
                "invalid inventory attribute",
                "path is empty string",
            ])
            self.assertEqual(expect, actual)
