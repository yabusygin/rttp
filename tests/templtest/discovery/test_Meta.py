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

from pathlib import Path
from textwrap import dedent
from unittest import TestCase

from packaging.version import Version

from templtest.discovery import Meta
from templtest.exception import TestDefinitionError

from ...util import change_working_directory, TempDirectory


class LoadTestMeta(TestCase):

    def test_default_path(self):
        with TempDirectory() as tmpdir_path:
            tests_path = Path(tmpdir_path, "templates_tests")
            tests_path.mkdir()
            meta_path = Path(tests_path, "meta.yml")
            meta_path.write_text(
                dedent(
                    """\
                    ---
                    version: "1.0"
                    """,
                ),
            )
            with change_working_directory(tmpdir_path):
                meta = Meta.load()

        actual = meta.version
        expect = Version("1.0")
        self.assertEqual(expect, actual)

    def test_custom_path(self):
        with TempDirectory() as tmpdir_path:
            meta_path = Path(tmpdir_path, "meta.yml")
            meta_path.write_text(
                dedent(
                    """\
                    ---
                    version: "1.0"
                    """,
                ),
            )
            meta = Meta.load(base_path=tmpdir_path)

        actual = meta.version
        expect = Version("1.0")
        self.assertEqual(expect, actual)

    def test_file_not_found(self):
        with TempDirectory() as tmpdir_path:
            with self.assertRaises(TestDefinitionError) as ctxmgr:
                Meta.load(base_path=tmpdir_path)

            actual = ctxmgr.exception.args[0]
            expect = "meta is not defined"
            self.assertEqual(expect, actual)

    def test_invalid_yaml_formatting(self):
        with TempDirectory() as tmpdir_path:
            meta_path = Path(tmpdir_path, "meta.yml")
            meta_path.write_text("@!%$#")

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                Meta.load(base_path=tmpdir_path)

            actual = ctxmgr.exception.args[0]
            expect = "meta is badly formatted"
            self.assertEqual(expect, actual)

    def test_invalid_meta_formatting(self):
        with TempDirectory() as tmpdir_path:
            meta_path = Path(tmpdir_path, "meta.yml")
            meta_path.write_text(
                dedent(
                    """\
                    ---
                    "1.0"
                    """,
                ),
            )

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                Meta.load(base_path=tmpdir_path)

            actual = ctxmgr.exception.args[0]
            expect = "meta is not a dictionary"
            self.assertEqual(expect, actual)

    def test_unspecified_version(self):
        with TempDirectory() as tmpdir_path:
            meta_path = Path(tmpdir_path, "meta.yml")
            meta_path.write_text(
                dedent(
                    """\
                    ---
                    {}
                    """,
                ),
            )

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                Meta.load(base_path=tmpdir_path)

            actual = ctxmgr.exception.args[0]
            expect = "testing speification version is not specified"
            self.assertEqual(expect, actual)

    def test_invalid_version_1(self):
        with TempDirectory() as tmpdir_path:
            meta_path = Path(tmpdir_path, "meta.yml")
            meta_path.write_text(
                dedent(
                    """\
                    ---
                    version: 1.0
                    """,
                ),
            )

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                Meta.load(base_path=tmpdir_path)

            actual = ctxmgr.exception.args[0]
            expect = "invalid testing speification version"
            self.assertEqual(expect, actual)

    def test_invalid_version_2(self):
        with TempDirectory() as tmpdir_path:
            meta_path = Path(tmpdir_path, "meta.yml")
            meta_path.write_text(
                dedent(
                    """\
                    ---
                    version: invalid
                    """,
                ),
            )

            with self.assertRaises(TestDefinitionError) as ctxmgr:
                Meta.load(base_path=tmpdir_path)

            actual = ctxmgr.exception.args[0]
            expect = "invalid testing speification version"
            self.assertEqual(expect, actual)
