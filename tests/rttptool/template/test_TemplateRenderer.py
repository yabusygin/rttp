# pylint: disable=invalid-name

from pathlib import Path
from unittest import TestCase

from rttptool.template import TemplateRenderer

from ...util import extract_role, TempDirectory


class TestTemplateRenderer(TestCase):

    def test_without_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "without_variable_definition"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(template=Path("foo.j2"))
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_defaults_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_defaults")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(template=Path("foo.j2"))
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_defaults_variable_definition_alt_filename_1(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_alt_filename_1"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_defaults")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(template=Path("foo.j2"))
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_defaults_variable_definition_alt_filename_2(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_alt_filename_2"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_defaults")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(template=Path("foo.j2"))
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_inventory_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_inventory")
            inventory_path = Path(test_path, "inventory.yml")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(
                template=Path("foo.j2"),
                inventory=inventory_path,
            )
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_vars_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_and_vars"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_vars")
            inventory_path = Path(test_path, "inventory.yml")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(
                template=Path("foo.j2"),
                inventory=inventory_path,
            )
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_vars_variable_definition_alt_filename_1(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_and_vars_alt_filename_1"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_vars")
            inventory_path = Path(test_path, "inventory.yml")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(
                template=Path("foo.j2"),
                inventory=inventory_path,
            )
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_vars_variable_definition_alt_filename_2(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_and_vars_alt_filename_2"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_vars")
            inventory_path = Path(test_path, "inventory.yml")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(
                template=Path("foo.j2"),
                inventory=inventory_path,
            )
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)

    def test_extra_variable_definition(self):
        with TempDirectory() as tmpdir_path:
            role_name = "with_defaults_and_vars"
            extract_role(role_name, tmpdir_path)
            role_path = Path(tmpdir_path, role_name)
            test_path = Path(role_path, "templates_tests", "test_extra")
            inventory_path = Path(test_path, "inventory.yml")
            extra_path = Path(test_path, "extra.yml")
            expect_path = Path(test_path, "foo")

            renderer = TemplateRenderer(role=role_path)
            actual = renderer.render(
                template=Path("foo.j2"),
                inventory=inventory_path,
                extra=extra_path,
            )
            expect = expect_path.read_text()
            self.assertEqual(expect, actual)
