from argparse import Namespace
from pathlib import Path
from unittest import TestCase

from rttptool.cli import _parse_args


class ParseArguments(TestCase):

    def test_default_args(self):
        actual = _parse_args([])
        expect = Namespace(role_path=Path("."))
        self.assertEqual(expect, actual)

    def test_custom_role_path(self):
        actual = _parse_args(["--role-path=test"])
        expect = Namespace(role_path=Path("test"))
        self.assertEqual(expect, actual)
