# templtest -- a tool for testing Ansible role templates
# Copyright (C) 2021-2023  Alexey Busygin
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

from argparse import Namespace
from contextlib import redirect_stdout, ExitStack
from io import StringIO
from pathlib import Path
from textwrap import dedent

from pytest import raises

from templtest.cli import _parse_args, main


def test_parse_args():
    assert Namespace(role_path=Path(".")) == _parse_args([])
    assert Namespace(role_path=Path("test")) == _parse_args(["--role-path=test"])


class TestMain:
    def test_success(self, resources):
        role_path = Path(resources, "roles", "with_defaults")

        with redirect_stdout(StringIO()) as stdout:
            main(argv=[f"--role-path={role_path}"])

        actual = stdout.getvalue()
        expect = dedent(
            """\
            [test.yml] test variable definition in role "defaults/" ... ok
            [test.yml] test variable definition in inventory ... ok
            """
        )
        assert expect == actual

    def test_faiure(self, resources):
        role_path = Path(resources, "roles", "test_failure")

        with ExitStack() as stack:
            stdout = stack.enter_context(redirect_stdout(StringIO()))
            excinfo = stack.enter_context(raises(SystemExit))

            main(argv=[f"--role-path={role_path}"])

        actual = stdout.getvalue()
        expect = dedent(
            """\
            [test.yml] this test fails ... fail
            --- templates_tests/foo
            +++ render(templates/foo.j2)
            @@ -1 +1 @@
            -baz
            +bar
            """
        )
        assert expect == actual

        assert 1 == excinfo.value.code

    def test_invalid_test_definition(self, resources):
        role_path = Path(resources, "roles", "invalid_path_in_test_definition")

        with ExitStack() as stack:
            stdout = stack.enter_context(redirect_stdout(StringIO()))
            excinfo = stack.enter_context(raises(SystemExit))

            main(argv=[f"--role-path={role_path}"])

        actual = stdout.getvalue()
        expect = ": ".join(
            [
                "TestDefinitionError",
                "invalid definition file 'test.yml'",
                "invalid test definition #0",
                "invalid variables attribute",
                "invalid inventory attribute",
                "path is empty string",
            ]
        )
        assert expect == actual

        assert 1 == excinfo.value.code
