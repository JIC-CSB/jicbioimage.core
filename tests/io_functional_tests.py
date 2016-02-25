"""BFConvertWrapper functional tests."""

import unittest
import os
import os.path
import shutil

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class MD5HashFunctionalTests(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_md5_from_file(self):
        from jicbioimage.core.io import _md5_hexdigest_from_file
        input_file = os.path.join(DATA_DIR, "tjelvar.png")
        self.assertEqual(_md5_hexdigest_from_file(input_file),
                         "894c9860e11667d29cdbf034e58ee75f")

    def test_md5_from_file_with_smaller_blocksize(self):
        from jicbioimage.core.io import _md5_hexdigest_from_file
        input_file = os.path.join(DATA_DIR, "tjelvar.png")
        self.assertEqual(_md5_hexdigest_from_file(input_file, 4096),
                         "894c9860e11667d29cdbf034e58ee75f")
