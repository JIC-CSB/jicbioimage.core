"""ProxyImage functional tests."""

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
        from jicimagelib.image import ProxyImage
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        proxy_image = ProxyImage(fpath, 0, 0, 0, 0)
        self.assertEqual(type(proxy_image._repr_png_()), bytes)
        

if __name__ == '__main__':
    unittest.main()
