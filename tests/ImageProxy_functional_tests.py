"""ImageProxy functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np
from skimage.io import imread, use_plugin

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')

class ImageUserStory(unittest.TestCase):
    
    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_repr_png_return_type(self):
        from jicimagelib.image import ImageProxy
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        image_proxy = ImageProxy(fpath, 0, 0, 0, 0)
        self.assertEqual(type(image_proxy._repr_png_()), bytes)
        

if __name__ == '__main__':
    unittest.main()
