"""Transform functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np
from skimage.io import imread, use_plugin

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class TransformationUserStory(unittest.TestCase):

    def setUp(self):
        from jicimagelib.io import AutoName
        AutoName.count = 0
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        from jicimagelib.io import AutoName
        AutoName.count = 0
        shutil.rmtree(TMP_DIR)


    def test_creating_transformations_from_scratch(self):
        
        # What if the default names of images was just the order in which they
        # were created?
        # Or perhaps the order + the function name, e.g.
        # 1_gaussian.png
        # 2_sobel.png
        # 3_gaussian.png
        # The order could be tracked in a class variable in an AutoName
        # object. The AutoName object could also store the output directory
        # as a class variable.

        from jicimagelib.image import Image
        from jicimagelib.transform import transformation
        from jicimagelib.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def identity(image):
            return image

        image = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))
        image = identity(image)
        self.assertEqual(image.history[-1], 'Applied identity transform')
        created_fpath = os.path.join(TMP_DIR, '1_identity.png')
        self.assertTrue(os.path.isfile(created_fpath),
            'No such file: {}'.format(created_fpath))

    def test_BZ2(self):
        from skimage.filters import gaussian_filter

        from jicimagelib.image import Image
        from jicimagelib.transform import transformation
        from jicimagelib.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def blur(image):
            return gaussian_filter(image, sigma=2)

        image = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))
        image = blur(image)

        # Image returned is of jicimagelib.image.Image type.
        self.assertTrue(isinstance(image, Image))

        # Image returned contains the history.
        self.assertEqual(image.history[-1], 'Applied blur transform')

        created_fpath = os.path.join(TMP_DIR, '1_blur.png')
        self.assertTrue(os.path.isfile(created_fpath),
            'No such file: {}'.format(created_fpath))

if __name__ == '__main__':
    unittest.main()
