# pylint: disable=invalid-name

from pathlib import Path
from unittest import TestCase

from templtest.discovery import TestDefinition, Variables
from templtest.exception import TestDefinitionError


class CheckInventory(TestCase):

    def test_present(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(
                inventory=Path("inventory.yml"),
                extra=None,
            ),
            expected_result=Path("foo"),
        )
        self.assertTrue(testdef.has_inventory())

    def test_absent(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(
                inventory=None,
                extra=None,
            ),
            expected_result=Path("foo"),
        )
        self.assertFalse(testdef.has_inventory())


class CheckExtra(TestCase):

    def test_present(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(
                inventory=None,
                extra=Path("extra.yml"),
            ),
            expected_result=Path("foo"),
        )
        self.assertTrue(testdef.has_extra())

    def test_absent(self):
        testdef = TestDefinition(
            name="test",
            template=Path("foo.j2"),
            variables=Variables(
                inventory=None,
                extra=None,
            ),
            expected_result=Path("foo"),
        )
        self.assertFalse(testdef.has_extra())


class CreateTestDefinition(TestCase):

    def test_without_variables_1(self):
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
        self.assertEqual(expect, actual)

    def test_without_variables_2(self):
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
        self.assertEqual(expect, actual)

    def test_with_variables(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
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
        self.assertEqual(expect, actual)

    def test_invalid_type(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document=[])
        actual = ctxmgr.exception.args[0]
        expect = "test definition is not a dictionary"
        self.assertEqual(expect, actual)

    def test_invalid_key_type(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
            1: "test",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "key is not a string"
        self.assertEqual(expect, actual)

    def test_unknown_key(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
            "unknown": "test",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "unknown attribute: unknown"
        self.assertEqual(expect, actual)

    def test_invalid_name_type(self):
        document = {
            "name": 1,
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "name is not a string"
        self.assertEqual(expect, actual)

    def test_unspecified_name_1(self):
        document = {
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "name is not specified"
        self.assertEqual(expect, actual)

    def test_unspecified_name_2(self):
        document = {
            "name": None,
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "name is not specified"
        self.assertEqual(expect, actual)

    def test_invalid_template(self):
        document = {
            "name": "test",
            "template": "",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "invalid template attribute"
        self.assertEqual(expect, actual)

    def test_unspecified_template_1(self):
        document = {
            "name": "test",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "template is not specified"
        self.assertEqual(expect, actual)

    def test_unspecified_template_2(self):
        document = {
            "name": "test",
            "template": None,
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "document",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "template is not specified"
        self.assertEqual(expect, actual)

    def test_invalid_variables(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {
                "inventory": "",
                "extra": "extra.yml",
            },
            "expected_result": "document",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "invalid variables attribute"
        self.assertEqual(expect, actual)

    def test_invalid_expected_result(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": "",
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "invalid expected result attribute"
        self.assertEqual(expect, actual)

    def test_unspecified_expected_result_1(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "expected result is not specified"
        self.assertEqual(expect, actual)

    def test_unspecified_expected_result_2(self):
        document = {
            "name": "test",
            "template": "document.j2",
            "variables": {
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
            "expected_result": None,
        }
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            TestDefinition.create(document)
        actual = ctxmgr.exception.args[0]
        expect = "expected result is not specified"
        self.assertEqual(expect, actual)
