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

from contextlib import chdir
from pathlib import Path

from packaging.version import Version
from pytest import raises

from templtest.discovery import (
    _create_path,
    _iter_testdefs,
    discover_tests,
    Meta,
    TestDefinition,
    Variables,
)
from templtest.exception import TestDefinitionError


class TestMeta:
    def test_default_path(self, resources):
        role_path = Path(resources, "roles", "with_defaults")

        with chdir(role_path):
            meta = Meta.load()

        assert Version("0.1") == meta.version

    def test_custom_path(self, resources):
        tests_path = Path(resources, "roles", "with_defaults", "templates_tests")

        meta = Meta.load(base_path=tests_path)

        assert Version("0.1") == meta.version

    def test_file_not_found(self, tmp_path):
        with raises(TestDefinitionError) as excinfo:
            Meta.load(base_path=tmp_path)

        actual = excinfo.value.args[0]
        expect = "meta is not defined"
        assert expect == actual

    def test_invalid_yaml(self, resources):
        tests_path = Path(resources, "invalid_meta", "invalid_yaml")

        with raises(TestDefinitionError) as excinfo:
            Meta.load(base_path=tests_path)

        actual = excinfo.value.args[0]
        expect = "meta is badly formatted"
        assert expect == actual

    def test_not_dictionary(self, resources):
        tests_path = Path(resources, "invalid_meta", "not_dictionary")

        with raises(TestDefinitionError) as excinfo:
            Meta.load(base_path=tests_path)

        actual = excinfo.value.args[0]
        expect = "meta is not a dictionary"
        assert expect == actual

    def test_missing_version(self, resources):
        tests_path = Path(resources, "invalid_meta", "missing_version")

        with raises(TestDefinitionError) as excinfo:
            Meta.load(base_path=tests_path)

        actual = excinfo.value.args[0]
        expect = "testing speification version is not specified"
        assert expect == actual

    def test_invalid_version_type(self, resources):
        tests_path = Path(resources, "invalid_meta", "invalid_version_type")

        with raises(TestDefinitionError) as excinfo:
            Meta.load(base_path=tests_path)

        actual = excinfo.value.args[0]
        expect = "invalid testing speification version"
        assert expect == actual

    def test_invalid_version_value(self, resources):
        tests_path = Path(resources, "invalid_meta", "invalid_version_value")

        with raises(TestDefinitionError) as excinfo:
            Meta.load(base_path=tests_path)

        actual = excinfo.value.args[0]
        expect = "invalid testing speification version"
        assert expect == actual


class TestVariables:
    def test_empty_1(self):
        actual = Variables.create(document={})
        expect = Variables(inventory=None, extra=None)
        assert expect == actual

    def test_empty_2(self):
        actual = Variables.create(document={"inventory": None, "extra": None})
        expect = Variables(inventory=None, extra=None)
        assert expect == actual

    def test_fully_specified(self):
        actual = Variables.create(
            document={"inventory": "inventory.yml", "extra": "extra.yml"}
        )
        expect = Variables(inventory=Path("inventory.yml"), extra=Path("extra.yml"))
        assert expect == actual

    def test_invalid_type(self):
        with raises(TestDefinitionError) as excinfo:
            Variables.create(document="variables.yml")

        actual = excinfo.value.args[0]
        expect = "variables attribute is not a dictionary"
        assert expect == actual

    def test_invalid_key_type(self):
        with raises(TestDefinitionError) as excinfo:
            Variables.create(
                document={"inventory": "inventory.yml", "extra": "extra.yml", 1: "bar"}
            )

        actual = excinfo.value.args[0]
        expect = "key is not a string"
        assert expect == actual

    def test_unknown_attribute(self):
        with raises(TestDefinitionError) as excinfo:
            Variables.create(
                document={
                    "inventory": "inventory.yml",
                    "extra": "extra.yml",
                    "foo": "bar",
                }
            )

        actual = excinfo.value.args[0]
        expect = "unknown attribute: foo"
        assert expect == actual

    def test_invalid_inventory(self):
        with raises(TestDefinitionError) as excinfo:
            Variables.create(
                document={
                    "inventory": "/absolute/path/to/inventory.yml",
                    "extra": "extra.yml",
                }
            )

        actual = excinfo.value.args[0]
        expect = "invalid inventory attribute"
        assert expect == actual

    def test_invalid_extra(self):
        with raises(TestDefinitionError) as excinfo:
            Variables.create(
                document={
                    "inventory": "inventory.yml",
                    "extra": "/absolute/path/to/extra.yml",
                }
            )

        actual = excinfo.value.args[0]
        expect = "invalid extra attribute"
        assert expect == actual


class TestTestDefinition:
    def test_inventory_present(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(inventory=Path("inventory.yml"), extra=None),
            expected_result=Path("foo"),
        )

        assert testdef.has_inventory()

    def test_inventory_absent(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(inventory=None, extra=None),
            expected_result=Path("foo"),
        )

        assert not testdef.has_inventory()

    def test_extra_present(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(inventory=None, extra=Path("extra.yml")),
            expected_result=Path("foo"),
        )

        assert testdef.has_extra()

    def test_extra_absent(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(inventory=None, extra=None),
            expected_result=Path("foo"),
        )

        assert not testdef.has_extra()

    def test_create_without_variables_1(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "expected_result": "document",
        }

        actual = TestDefinition.create(document)
        expect = TestDefinition(
            name="test",
            template=Path("document.j2"),
            variables=None,
            expected_result=Path("document"),
        )
        assert expect == actual

    def test_create_without_variables_2(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": None,
            "expected_result": "document",
        }

        actual = TestDefinition.create(document)
        expect = TestDefinition(
            name="test",
            template=Path("document.j2"),
            variables=None,
            expected_result=Path("document"),
        )
        assert expect == actual

    def test_create_with_variables(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
        }

        actual = TestDefinition.create(document)
        expect = TestDefinition(
            name="test",
            template=Path("document.j2"),
            variables=Variables(
                inventory=Path("inventory.yml"),
                extra=Path("extra.yml"),
            ),
            expected_result=Path("document"),
        )
        assert expect == actual

    def test_create_invalid_type(self):
        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document=[])

        actual = excinfo.value.args[0]
        expect = "test definition is not a dictionary"
        assert expect == actual

    def test_create_invalid_key_type(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
            1: "test",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "key is not a string"
        assert expect == actual

    def test_create_unknown_key(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
            "unknown": "test",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "unknown attribute: unknown"
        assert expect == actual

    def test_create_invalid_name_type(self):
        document = {
            "name": 1,
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "name is not a string"
        assert expect == actual

    def test_create_unspecified_name_1(self):
        document = {
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "name is not specified"
        assert expect == actual

    def test_create_unspecified_name_2(self):
        document = {
            "name": None,
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "name is not specified"
        assert expect == actual

    def test_create_invalid_template(self):
        document = {
            "name": "test",
            "template": "",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "invalid template attribute"
        assert expect == actual

    def test_create_unspecified_template_1(self):
        document = {
            "name": "test",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "template is not specified"
        assert expect == actual

    def test_create_unspecified_template_2(self):
        document = {
            "name": "test",
            "template": None,
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "document",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "template is not specified"
        assert expect == actual

    def test_create_invalid_variables(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {"inventory": "", "extra": "extra.yml"},
            "expected_result": "document",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "invalid variables attribute"
        assert expect == actual

    def test_create_invalid_expected_result(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": "",
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "invalid expected result attribute"
        assert expect == actual

    def test_create_unspecified_expected_result_1(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "expected result is not specified"
        assert expect == actual

    def test_create_unspecified_expected_result_2(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
            "expected_result": None,
        }

        with raises(TestDefinitionError) as excinfo:
            TestDefinition.create(document)

        actual = excinfo.value.args[0]
        expect = "expected result is not specified"
        assert expect == actual


class TestCreatePath:
    def test(self):
        actual = _create_path("path/to/file")
        expect = Path("path", "to", "file")
        assert expect == actual

    def test_invalid_type(self):
        with raises(TestDefinitionError) as excinfo:
            _create_path(None)

        actual = excinfo.value.args[0]
        expect = "path is not a string"
        assert expect == actual

    def test_empty_string(self):
        with raises(TestDefinitionError) as excinfo:
            _create_path("")

        actual = excinfo.value.args[0]
        expect = "path is empty string"
        assert expect == actual

    def test_absolute_path(self):
        with raises(TestDefinitionError) as excinfo:
            _create_path("/path/to/file")

        actual = excinfo.value.args[0]
        expect = "path is not relative"
        assert expect == actual


class TestIterTestdefs:
    def test_empty_1(self):
        actual = list(_iter_testdefs({"tests": None}))
        expect = []
        assert expect == actual

    def test_empty_2(self):
        actual = list(_iter_testdefs({"tests": []}))
        expect = []
        assert expect == actual

    def test_invalid_type(self):
        with raises(TestDefinitionError) as excinfo:
            list(_iter_testdefs([]))

        actual = excinfo.value.args[0]
        expect = "test definitions document is not a dictionary"
        assert expect == actual

    def test_invalid_key_type(self):
        with raises(TestDefinitionError) as excinfo:
            list(_iter_testdefs({1: "test"}))

        actual = excinfo.value.args[0]
        expect = "key is not a string"
        assert expect == actual

    def test_unknown_key(self):
        with raises(TestDefinitionError) as excinfo:
            list(_iter_testdefs({"tests": [], "unknown": "test"}))

        actual = excinfo.value.args[0]
        expect = "unknown attribute: unknown"
        assert expect == actual

    def test_invalid_tests_type(self):
        document = {
            "tests": {
                "name": "test",
                "template": "document.j2",
                "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
                "expected_result": "document",
            }
        }

        with raises(TestDefinitionError) as excinfo:
            list(_iter_testdefs(document))

        actual = excinfo.value.args[0]
        expect = "test definitions are not list"
        assert expect == actual

    def test_invalid_test_definition(self):
        document = {
            "tests": [
                {
                    "name": "test",
                    "template": "",
                    "variables": {"inventory": "inventory.yml", "extra": "extra.yml"},
                    "expected_result": "document",
                }
            ]
        }

        with raises(TestDefinitionError) as excinfo:
            list(_iter_testdefs(document))

        actual = excinfo.value.args[0]
        expect = "invalid test definition #0"
        assert expect == actual


class TestDiscoverTests:
    @staticmethod
    def get_path(item):
        return item[1]

    def test_default_path(self, resources):
        role_path = Path(resources, "roles", "multiple_files_with_test_definitions")

        with chdir(role_path):
            discovered = list(discover_tests())

        actual = {self.get_path(item) for item in discovered}
        expect = {
            Path("test.yml"),
            Path("test-bar.yml"),
            Path("subdir", "test.yml"),
            Path("subdir", "test-baz.yml"),
        }
        assert expect == actual

        actual = discovered[0][0]
        expect = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=None,
            expected_result=Path("foo"),
        )
        assert expect == actual

    def test_custom_path(self, resources):
        tests_path = Path(
            resources,
            "roles",
            "multiple_files_with_test_definitions",
            "templates_tests",
        )

        discovered = list(discover_tests(tests_path))

        actual = {self.get_path(item) for item in discovered}
        expect = {
            Path("test.yml"),
            Path("test-bar.yml"),
            Path("subdir", "test.yml"),
            Path("subdir", "test-baz.yml"),
        }
        assert expect == actual

    def test_badly_formatted_test_definition(self, resources):
        tests_path = Path(
            resources, "roles", "badly_formatted_test_definition", "templates_tests"
        )

        with raises(TestDefinitionError) as excinfo:
            next(discover_tests(tests_path))

        actual = excinfo.value.args[0]
        expect = " ".join(("test definition file 'test.yml' is badly formatted",))
        assert expect == actual

    def test_invalid_test_definition(self, resources):
        tests_path = Path(
            resources, "roles", "invalid_test_definition", "templates_tests"
        )

        with raises(TestDefinitionError) as excinfo:
            next(discover_tests(tests_path))

        actual = excinfo.value.args[0]
        expect = "invalid definition file 'test.yml'"
        assert expect == actual

    def test_metadata_error(self, resources):
        tests_path = Path(resources, "roles", "tests_metadata_error", "templates_tests")

        with raises(TestDefinitionError) as excinfo:
            next(discover_tests(tests_path))

        actual = excinfo.value.args[0]
        expect = "failed to get tests metadata"
        assert expect == actual

    def test_unsupported_version(self, resources):
        tests_path = Path(
            resources, "roles", "unsupported_tests_version", "templates_tests"
        )

        with raises(TestDefinitionError) as excinfo:
            next(discover_tests(tests_path))

        actual = excinfo.value.args[0]
        expect = "unsupported testing speification version"
        assert expect == actual
