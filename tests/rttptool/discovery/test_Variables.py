# pylint: disable=invalid-name

from pathlib import Path
from unittest import TestCase

from rttptool.discovery import Variables
from rttptool.exception import TestDefinitionError


class CreateVariables(TestCase):

    def test_empty_1(self):
        actual = Variables.create(document={})
        expect = Variables(
            inventory=None,
            extra=None,
        )
        self.assertEqual(expect, actual)

    def test_empty_2(self):
        actual = Variables.create(
            document={
                "inventory": None,
                "extra": None,
            },
        )
        expect = Variables(
            inventory=None,
            extra=None,
        )
        self.assertEqual(expect, actual)

    def test_fully_specified(self):
        actual = Variables.create(
            document={
                "inventory": "inventory.yml",
                "extra": "extra.yml",
            },
        )
        expect = Variables(
            inventory=Path("inventory.yml"),
            extra=Path("extra.yml"),
        )
        self.assertEqual(expect, actual)

    def test_invalid_type(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            Variables.create(document="variables.yml")
        actual = ctxmgr.exception.args[0]
        expect = "variables attribute is not a dictionary"
        self.assertEqual(expect, actual)

    def test_invalid_key_type(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            Variables.create(
                document={
                    "inventory": "inventory.yml",
                    "extra": "extra.yml",
                    1: "bar",
                },
            )
        actual = ctxmgr.exception.args[0]
        expect = "key is not a string"
        self.assertEqual(expect, actual)

    def test_unknown_attribute(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            Variables.create(
                document={
                    "inventory": "inventory.yml",
                    "extra": "extra.yml",
                    "foo": "bar",
                },
            )
        actual = ctxmgr.exception.args[0]
        expect = "unknown attribute: foo"
        self.assertEqual(expect, actual)

    def test_invalid_inventory(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            Variables.create(
                document={
                    "inventory": "/absolute/path/to/inventory.yml",
                    "extra": "extra.yml",
                },
            )
        actual = ctxmgr.exception.args[0]
        expect = "invalid inventory attribute"
        self.assertEqual(expect, actual)

    def test_invalid_extra(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            Variables.create(
                document={
                    "inventory": "inventory.yml",
                    "extra": "/absolute/path/to/extra.yml",
                },
            )
        actual = ctxmgr.exception.args[0]
        expect = "invalid extra attribute"
        self.assertEqual(expect, actual)
