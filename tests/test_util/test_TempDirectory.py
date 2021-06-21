# pylint: disable=invalid-name

from unittest import TestCase

from ..util import TempDirectory


class TestTempDirectory(TestCase):

    def test(self):
        with TempDirectory() as temp_dir_path:
            self.assertTrue(temp_dir_path.is_dir())
            self.assertTrue(temp_dir_path.name.startswith("rttptool.test."))
        self.assertFalse(temp_dir_path.exists())
