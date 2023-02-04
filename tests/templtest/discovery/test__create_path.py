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
