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

from argparse import Namespace
from pathlib import Path
from unittest import TestCase

from templtest.cli import _parse_args


class ParseArguments(TestCase):

    def test_default_args(self):
        actual = _parse_args([])
        expect = Namespace(role_path=Path("."))
        self.assertEqual(expect, actual)

    def test_custom_role_path(self):
        actual = _parse_args(["--role-path=test"])
        expect = Namespace(role_path=Path("test"))
        self.assertEqual(expect, actual)
