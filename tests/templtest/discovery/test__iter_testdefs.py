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

from unittest import TestCase

from templtest.discovery import _iter_testdefs
from templtest.exception import TestDefinitionError


class CreateTestDefinitionList(TestCase):
    def test_empty_1(self):
        document = {
            "tests": None,
        }
        actual = list(_iter_testdefs(document))
        expect = []
        self.assertEqual(expect, actual)

    def test_empty_2(self):
        document = {
            "tests": [],
        }
        actual = list(_iter_testdefs(document))
        expect = []
        self.assertEqual(expect, actual)

    def test_invalid_type(self):
        document = []
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            list(_iter_testdefs(document))
        actual = ctxmgr.exception.args[0]
        expect = "test definitions document is not a dictionary"
        self.assertEqual(expect, actual)

    def test_invalid_key_type(self):
        document = {
            1: "test",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            list(_iter_testdefs(document))
        actual = ctxmgr.exception.args[0]
        expect = "key is not a string"
        self.assertEqual(expect, actual)

    def test_unknown_key(self):
        document = {
            "tests": [],
            "unknown": "test",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            list(_iter_testdefs(document))
        actual = ctxmgr.exception.args[0]
        expect = "unknown attribute: unknown"
        self.assertEqual(expect, actual)

    def test_invalid_tests_type(self):
        document = {
            "tests": {
                "name": "test",
                "template": "document.j2",
                "variables": {
                    "inventory": "inventory.yml",
                    "extra": "extra.yml",
                },
                "expected_result": "document",
            },
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            list(_iter_testdefs(document))
        actual = ctxmgr.exception.args[0]
        expect = "test definitions are not list"
        self.assertEqual(expect, actual)

    def test_invalid_test_definition(self):
        document = {
            "tests": [
                {
                    "name": "test",
                    "template": "",
                    "variables": {
                        "inventory": "inventory.yml",
                        "extra": "extra.yml",
                    },
                    "expected_result": "document",
                },
            ],
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            list(_iter_testdefs(document))
        actual = ctxmgr.exception.args[0]
        expect = "invalid test definition #0"
        self.assertEqual(expect, actual)
