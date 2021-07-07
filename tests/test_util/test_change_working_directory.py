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

from ..util import change_working_directory, TempDirectory


class ChangeWorkingDirectory(TestCase):

    def test(self):
        with TempDirectory() as tempdir_path:
            cwd = Path.cwd()

            with change_working_directory(tempdir_path):
                actual = Path.cwd()
                expect = tempdir_path.resolve()
                self.assertEqual(expect, actual)

            actual = Path.cwd()
            expect = cwd
            self.assertEqual(expect, actual)

    def test_exception(self):
        with TempDirectory() as tempdir_path:
            cwd = Path.cwd()

            class TestException(Exception):
                pass

            with self.assertRaises(TestException):
                with change_working_directory(tempdir_path):
                    raise TestException()

            actual = Path.cwd()
            expect = cwd
            self.assertEqual(expect, actual)

    def test_change_to_non_existent(self):
        with TempDirectory() as tempdir_path:
            cwd = Path.cwd()

            non_existent_path = Path(tempdir_path, "non-existent")
            with self.assertRaises(FileNotFoundError):
                with change_working_directory(non_existent_path):
                    pass

            actual = Path.cwd()
            expect = cwd
            self.assertEqual(expect, actual)
