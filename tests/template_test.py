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

from pathlib import Path

from templtest.template import AnsibleTemplateRenderer, Jinja2TemplateRenderer


class TestJinja2TemplateRenderer:
    def test_without_variable_definition(self, resources):
        role_path = Path(resources, "roles", "without_variable_definition")
        test_path = Path(role_path, "templates_tests")

        actual = Jinja2TemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_defaults_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults")
        test_path = Path(role_path, "templates_tests", "test_defaults")

        actual = Jinja2TemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_defaults_variable_definition_alt_filename_1(self, resources):
        role_path = Path(resources, "roles", "with_defaults_alt_filename_1")
        test_path = Path(role_path, "templates_tests", "test_defaults")

        actual = Jinja2TemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_defaults_variable_definition_alt_filename_2(self, resources):
        role_path = Path(resources, "roles", "with_defaults_alt_filename_2")
        test_path = Path(role_path, "templates_tests", "test_defaults")

        actual = Jinja2TemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_inventory_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults")
        test_path = Path(role_path, "templates_tests", "test_inventory")

        actual = Jinja2TemplateRenderer(role=role_path).render(
            template=Path("foo.j2"),
            inventory=Path(test_path, "inventory.yml"),
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_vars_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars")
        test_path = Path(role_path, "templates_tests", "test_vars")

        actual = Jinja2TemplateRenderer(role=role_path).render(
            template=Path("foo.j2"),
            inventory=Path(test_path, "inventory.yml"),
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_vars_variable_definition_alt_filename_1(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars_alt_filename_1")
        test_path = Path(role_path, "templates_tests", "test_vars")

        actual = Jinja2TemplateRenderer(role=role_path).render(
            template=Path("foo.j2"), inventory=Path(test_path, "inventory.yml")
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_vars_variable_definition_alt_filename_2(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars_alt_filename_2")
        test_path = Path(role_path, "templates_tests", "test_vars")

        actual = Jinja2TemplateRenderer(role=role_path).render(
            template=Path("foo.j2"), inventory=Path(test_path, "inventory.yml")
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_extra_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars")
        test_path = Path(role_path, "templates_tests", "test_extra")

        actual = Jinja2TemplateRenderer(role=role_path).render(
            template=Path("foo.j2"),
            inventory=Path(test_path, "inventory.yml"),
            extra=Path(test_path, "extra.yml"),
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual


class TestAnsibleTemplateRenderer:
    def test_without_variable_definition(self, resources):
        role_path = Path(resources, "roles", "without_variable_definition")
        test_path = Path(role_path, "templates_tests")

        actual = AnsibleTemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_defaults_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults")
        test_path = Path(role_path, "templates_tests", "test_defaults")

        actual = AnsibleTemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_defaults_variable_definition_alt_filename_1(self, resources):
        role_path = Path(resources, "roles", "with_defaults_alt_filename_1")
        test_path = Path(role_path, "templates_tests", "test_defaults")

        actual = AnsibleTemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_defaults_variable_definition_alt_filename_2(self, resources):
        role_path = Path(resources, "roles", "with_defaults_alt_filename_2")
        test_path = Path(role_path, "templates_tests", "test_defaults")

        actual = AnsibleTemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_inventory_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults")
        test_path = Path(role_path, "templates_tests", "test_inventory")

        actual = AnsibleTemplateRenderer(role=role_path).render(
            template=Path("foo.j2"), inventory=Path(test_path, "inventory.yml")
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_vars_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars")
        test_path = Path(role_path, "templates_tests", "test_vars")

        actual = AnsibleTemplateRenderer(role=role_path).render(
            template=Path("foo.j2"), inventory=Path(test_path, "inventory.yml")
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_vars_variable_definition_alt_filename_1(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars_alt_filename_1")
        test_path = Path(role_path, "templates_tests", "test_vars")

        actual = AnsibleTemplateRenderer(role=role_path).render(
            template=Path("foo.j2"), inventory=Path(test_path, "inventory.yml")
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_vars_variable_definition_alt_filename_2(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars_alt_filename_2")
        test_path = Path(role_path, "templates_tests", "test_vars")

        actual = AnsibleTemplateRenderer(role=role_path).render(
            template=Path("foo.j2"), inventory=Path(test_path, "inventory.yml")
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_extra_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars")
        test_path = Path(role_path, "templates_tests", "test_extra")

        actual = AnsibleTemplateRenderer(role=role_path).render(
            template=Path("foo.j2"),
            inventory=Path(test_path, "inventory.yml"),
            extra=Path(test_path, "extra.yml"),
        )
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_ansible_filter(self, resources):
        role_path = Path(resources, "roles", "ansible_filter")
        test_path = Path(role_path, "templates_tests")

        actual = AnsibleTemplateRenderer(role=role_path).render(template=Path("foo.j2"))
        expect = Path(test_path, "foo").read_text(encoding="utf-8")
        assert expect == actual

    def test_json_template(self, resources):
        role_path = Path(resources, "roles", "json_template")
        test_path = Path(role_path, "templates_tests")

        actual = AnsibleTemplateRenderer(role=role_path).render(
            template=Path("foo.json.j2")
        )
        expect = Path(test_path, "foo.json").read_text(encoding="utf-8")
        assert expect == actual
