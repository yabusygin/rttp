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
from textwrap import dedent

from pytest import raises

from templtest.discovery import TestDefinition, Variables
from templtest.exception import AssertError
from templtest.test import Test


class TestTest:
    def test_inventory_path_present(self):
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
        actual = test._inventory_path  # pylint: disable=protected-access
        assert expect == actual

    def test_inventory_path_absent(self):
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
        assert test._inventory_path is None  # pylint: disable=protected-access

    def test_extra_path_present(self):
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
        actual = test._extra_path  # pylint: disable=protected-access
        assert expect == actual

    def test_extra_path_absent(self):
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
        assert test._extra_path is None  # pylint: disable=protected-access

    def test_base_path_absolute_src(self):
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
        actual = test._base_path  # pylint: disable=protected-access
        assert expect == actual

    def test_base_path_relative_src(self):
        role_path = Path("/", "home", "user", "ansible", "role")
        tests_path = Path(role_path, "templates_tests")
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
        expect = tests_path
        actual = test._base_path  # pylint: disable=protected-access
        assert expect == actual

    def test_run_without_variable_definition(self, resources):
        role_path = Path(resources, "roles", "without_variable_definition")

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

    def test_defaults_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults")

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

    def test_inventory_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults")

        test = Test(
            role_path=role_path,
            src_path=Path("test.yml"),
            testdef=TestDefinition(
                name="test",
                template=Path("foo.j2"),
                variables=Variables(
                    inventory=Path("test_inventory", "inventory.yml"), extra=None
                ),
                expected_result=Path("test_inventory", "foo"),
            ),
        )
        test.run()

    def test_vars_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars")

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

    def test_extra_variable_definition(self, resources):
        role_path = Path(resources, "roles", "with_defaults_and_vars")

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

    def test_failure(self, resources):
        role_path = Path(resources, "roles", "test_failure")

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
        with raises(AssertError) as excinfo:
            test.run()

        assert 1 == len(excinfo.value.args)

        actual = excinfo.value.args[0]
        expect = dedent(
            """\
            --- templates_tests/foo
            +++ render(templates/foo.j2)
            @@ -1 +1 @@
            -baz
            +bar""",
        )
        assert expect == actual
