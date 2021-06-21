# pylint: disable=invalid-name

from pathlib import Path
from textwrap import dedent
from unittest import TestCase

from rttptool.discovery import TestDefinition, Variables
from rttptool.exception import AssertError
from rttptool.test import Test

from ...util import extract_role, TempDirectory


class GetInventoryPath(TestCase):
    # pylint: disable=protected-access

    def test_present(self):
        role_path = Path("/", "home", "user", "ansible", "role")
        tests_path = Path(role_path, "templates_tests")
        test = Test(
            role_path=role_path,
            src_path=Path(tests_path, "test.yml"),
            testdef=TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=Variables(
                    inventory=Path("inventory.yml"),
                    extra=None,
                ),
                expected_result=Path("foo"),
            ),
        )
        expect = Path(tests_path, "inventory.yml")
        actual = test._inventory_path
        self.assertEqual(expect, actual)

    def test_absent(self):
        role_path = Path("/", "home", "user", "ansible", "role")
        tests_path = Path(role_path, "templates_tests")
        test = Test(
            role_path=role_path,
            src_path=Path(tests_path, "test.yml"),
            testdef=TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=Variables(
                    inventory=None,
                    extra=None,
                ),
                expected_result=Path("foo"),
            ),
        )
        self.assertIsNone(test._inventory_path)


class GetExtraPath(TestCase):
    # pylint: disable=protected-access

    def test_present(self):
        role_path = Path("/", "home", "user", "ansible", "role")
        tests_path = Path(role_path, "templates_tests")
        test = Test(
            role_path=role_path,
            src_path=Path(tests_path, "test.yml"),
            testdef=TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=Variables(
                    inventory=None,
                    extra=Path("extra.yml"),
                ),
                expected_result=Path("foo"),
            ),
        )
        expect = Path(tests_path, "extra.yml")
        actual = test._extra_path
        self.assertEqual(expect, actual)

    def test_absent(self):
        role_path = Path("/", "home", "user", "ansible", "role")
        tests_path = Path(role_path, "templates_tests")
        test = Test(
            role_path=role_path,
            src_path=Path(tests_path, "test.yml"),
            testdef=TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=Variables(
                    inventory=None,
                    extra=None,
                ),
                expected_result=Path("foo"),
            ),
        )
        self.assertIsNone(test._extra_path)


class GetBasePath(TestCase):
    # pylint: disable=protected-access

    def test_absolute_src(self):
        role_path = Path("/", "home", "user", "ansible", "role")
        tests_path = Path(role_path, "templates_tests")
        test = Test(
            role_path=role_path,
            src_path=Path(tests_path, "test.yml"),
            testdef=TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=None,
                expected_result=Path("foo"),
            ),
        )
        expect = tests_path
        actual = test._base_path
        self.assertEqual(expect, actual)

    def test_relative_src(self):
        role_path = Path("/", "home", "user", "ansible", "role")
        tests_path = Path(role_path, "templates_tests")
        test = Test(
            role_path=role_path,
            src_path=Path(tests_path, "test.yml"),
            testdef=TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=None,
                expected_result=Path("foo"),
            ),
        )
        expect = tests_path
        actual = test._base_path
        self.assertEqual(expect, actual)


class RunTestCase(TestCase):
    # pylint: disable=no-self-use

    def test_without_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "without_variable_definition"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test = Test(
                role_path=role_path,
                src_path=Path("test.yml"),
                testdef=TestDefinition(
                    name="test",
                    template=Path("foo.j2"),
                    variables=None,
                    expected_result=Path("foo"),
                ),
            )
            test.run()

    def test_defaults_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test = Test(
                role_path=role_path,
                src_path=Path("test.yml"),
                testdef=TestDefinition(
                    name="test",
                    template=Path("foo.j2"),
                    variables=None,
                    expected_result=Path("test_defaults", "foo"),
                ),
            )
            test.run()

    def test_inventory_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test = Test(
                role_path=role_path,
                src_path=Path("test.yml"),
                testdef=TestDefinition(
                    name="test",
                    template=Path("foo.j2"),
                    variables=Variables(
                        inventory=Path("test_inventory", "inventory.yml"),
                        extra=None,
                    ),
                    expected_result=Path("test_inventory", "foo"),
                ),
            )
            test.run()

    def test_vars_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_and_vars"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test = Test(
                role_path=role_path,
                src_path=Path("test.yml"),
                testdef=TestDefinition(
                    name="test",
                    template=Path("foo.j2"),
                    variables=Variables(
                        inventory=Path("test_vars", "inventory.yml"),
                        extra=None,
                    ),
                    expected_result=Path("test_vars", "foo"),
                ),
            )
            test.run()

    def test_extra_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_and_vars"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test = Test(
                role_path=role_path,
                src_path=Path("test.yml"),
                testdef=TestDefinition(
                    name="test",
                    template=Path("foo.j2"),
                    variables=Variables(
                        inventory=Path("test_extra", "inventory.yml"),
                        extra=Path("test_extra", "extra.yml"),
                    ),
                    expected_result=Path("test_extra", "foo"),
                ),
            )
            test.run()

    def test_failure(self):
        with TempDirectory() as tmpdir_path:
            role_name = "test_failure"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test = Test(
                role_path=role_path,
                src_path=Path("test.yml"),
                testdef=TestDefinition(
                    name="test",
                    template=Path("foo.j2"),
                    variables=None,
                    expected_result=Path("foo"),
                ),
            )
            with self.assertRaises(AssertError) as ctxmgr:
                test.run()
            exc = ctxmgr.exception

            self.assertEqual(1, len(exc.args))

            actual = exc.args[0]
            expect = dedent(
                """\
                --- templates_tests/foo
                +++ render(templates/foo.j2)
                @@ -1 +1 @@
                -baz
                +bar""",
            )
            self.assertEqual(expect, actual)
