from pathlib import Path
from unittest import TestCase

from rttptool.discovery import discover_tests, TestDefinition
from rttptool.exception import TestDefinitionError

from ...util import change_working_directory, extract_role, TempDirectory


class DiscoverTests(TestCase):

    def test_default_path(self):
        with TempDirectory() as tmpdir_path:
            role_name = "multiple_files_with_test_definitions"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)

            with change_working_directory(role_path):
                discovered = list(discover_tests())

            def get_path(item):
                return item[1]

            actual = {
                get_path(item)
                for item in discovered
            }
            expect = {
                Path("test.yml"),
                Path("test-bar.yml"),
                Path("subdir", "test.yml"),
                Path("subdir", "test-baz.yml"),
            }
            self.assertEqual(expect, actual)

            actual = discovered[0][0]
            expect = TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=None,
                expected_result=Path("foo"),
            )
            self.assertEqual(expect, actual)

    def test_custom_path(self):
        with TempDirectory() as tmpdir_path:
            role_name = "multiple_files_with_test_definitions"
            extract_role(role_name, tmpdir_path)
            tests_path = Path(tmpdir_path, role_name, "templates_tests")

            discovered = list(discover_tests(tests_path))

            def get_path(item):
                return item[1]

            actual = {
                get_path(item)
                for item in discovered
            }
            expect = {
                Path("test.yml"),
                Path("test-bar.yml"),
                Path("subdir", "test.yml"),
                Path("subdir", "test-baz.yml"),
            }
            self.assertEqual(expect, actual)

    def test_badly_formatted_test_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "badly_formatted_test_definition"
            extract_role(role_name, tmpdir_path)
            tests_path = Path(tmpdir_path, role_name, "templates_tests")

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                next(discover_tests(tests_path))
            actual = ctxmgr.exception.args[0]
            expect = " ".join((
                "test definition file 'test.yml' is badly formatted",
            ))
            self.assertEqual(expect, actual)

    def test_invalid_test_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "invalid_test_definition"
            extract_role(role_name, tmpdir_path)
            tests_path = Path(tmpdir_path, role_name, "templates_tests")

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                next(discover_tests(tests_path))
            actual = ctxmgr.exception.args[0]
            expect = "invalid definition file 'test.yml'"
            self.assertEqual(expect, actual)

    def test_metadata_error(self):
        with TempDirectory() as tmpdir_path:
            role_name = "tests_metadata_error"
            extract_role(role_name, tmpdir_path)
            tests_path = Path(tmpdir_path, role_name, "templates_tests")

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                next(discover_tests(tests_path))
            actual = ctxmgr.exception.args[0]
            expect = "failed to get tests metadata"
            self.assertEqual(expect, actual)

    def test_unsupported_version(self):
        with TempDirectory() as tmpdir_path:
            role_name = "unsupported_tests_version"
            extract_role(role_name, tmpdir_path)
            tests_path = Path(tmpdir_path, role_name, "templates_tests")

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                next(discover_tests(tests_path))
            actual = ctxmgr.exception.args[0]
            expect = "unsupported RTTP version"
            self.assertEqual(expect, actual)
