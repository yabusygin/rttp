from unittest import TestCase

from rttptool.discovery import _iter_testdefs
from rttptool.exception import TestDefinitionError


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
