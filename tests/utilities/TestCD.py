from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import unittest
import os
import tempfile
from mri.utilities import cd


class TestCD(unittest.TestCase):
    def test_cd(self):
        tempdir = tempfile.gettempdir()
        with cd(tempdir):
            cwd = os.getcwd()
            self.assertEqual(cwd, tempfile.tempdir)


if __name__ == '__main__':
    unittest.main()
