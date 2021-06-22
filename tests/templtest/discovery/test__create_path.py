from pathlib import Path
from unittest import TestCase

from templtest.discovery import _create_path
from templtest.exception import TestDefinitionError


class CreatePath(TestCase):

    def test(self):
        actual = _create_path("path/to/file")
        expect = Path("path", "to", "file")
        self.assertEqual(expect, actual)

    def test_invalid_type(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            _create_path(None)
        actual = ctxmgr.exception.args[0]
        expect = "path is not a string"
        self.assertEqual(expect, actual)

    def test_empty_string(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            _create_path("")
        actual = ctxmgr.exception.args[0]
        expect = "path is empty string"
        self.assertEqual(expect, actual)

    def test_absolute_path(self):
        with self.assertRaises(TestDefinitionError) as ctxmgr:
            _create_path("/path/to/file")
        actual = ctxmgr.exception.args[0]
        expect = "path is not relative"
        self.assertEqual(expect, actual)
