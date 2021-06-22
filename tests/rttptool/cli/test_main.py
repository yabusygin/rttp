from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from textwrap import dedent
from unittest import TestCase

from rttptool.cli import main

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
