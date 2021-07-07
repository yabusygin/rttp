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

from contextlib import contextmanager
from itertools import chain
from os import chdir
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from types import TracebackType
from typing import Iterator, List, Optional, Type

try:
    # pylint: disable=unused-import
    # Mypy type checking is currently disabled. See issue #1153.
    from importlib.resources import (   # type: ignore
        path as resource_path,
        read_text,
    )
except ImportError:
    # pylint: disable=unused-import
    # Mypy type checking is currently disabled. See issue #1153.
    from importlib_resources import (   # type: ignore
        path as resource_path,
        read_text,
    )

from yaml import safe_load


class TempDirectory:

    PREFIX = "templtest.test."

    def __init__(self):
        # pylint: disable=consider-using-with
        self._tempdir = TemporaryDirectory(prefix=self.PREFIX)

    def __enter__(self) -> Path:
        return Path(self._tempdir.__enter__())

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:
        return self._tempdir.__exit__(exc_type, exc_value, traceback)


def _get_role_files(name: str) -> List[str]:
    data = read_text(".".join([__package__, "resources", "roles"]), "meta.yml")
    document = safe_load(data)
    matched = [
        role_meta
        for role_meta in document["roles"]
        if role_meta["name"] == name
    ]
    if not matched:
        raise KeyError("role '{}' meta is not found".format(name))
    return matched[0]["files"]


def _copy_role_resource(src: Path, dest: Path) -> None:
    roles_package = ".".join([__package__, "resources", "roles"])
    package = roles_package \
        if src.parent == Path(".") \
        else ".".join(chain([roles_package], src.parent.parts))
    with resource_path(package, src.name) as path:
        copyfile(path, dest)


def extract_role(name: str, dest: Path) -> None:
    for role_file in _get_role_files(name):
        if role_file.endswith("/"):
            Path(dest, role_file).mkdir(parents=True)
        else:
            _copy_role_resource(Path(role_file), Path(dest, role_file))


@contextmanager
def change_working_directory(path: Path) -> Iterator[None]:
    old_working_directory = Path.cwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(old_working_directory)
