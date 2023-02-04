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

# pylint: disable=invalid-name

from unittest import TestCase

from ..util import TempDirectory


class TestTempDirectory(TestCase):
    def test(self):
        with TempDirectory() as temp_dir_path:
            self.assertTrue(temp_dir_path.is_dir())
            self.assertTrue(temp_dir_path.name.startswith("templtest.test."))
        self.assertFalse(temp_dir_path.exists())
