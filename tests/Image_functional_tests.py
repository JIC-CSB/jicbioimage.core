"""Image functional tests."""

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

    def test_manual_image_creation_from_file(self):

        from jicbioimage.core.image import Image

        # Preamble: let us define the path to a TIFF file and create a numpy
        # array from it.
#       from libtiff import TIFF
#       tif = TIFF.open(path_to_tiff, 'r')
#       ar = tif.read_image()
        path_to_tiff = os.path.join(DATA_DIR, 'single-channel.ome.tif')
        use_plugin('freeimage')
        ar = imread(path_to_tiff)


        # It is possible to create an image from a file.
        image = Image.from_file(path_to_tiff)
        self.assertEqual(image.history[0],
                         'Created Image from {}'.format(path_to_tiff))

        # With name...
        image = Image.from_file(path_to_tiff, name='Test1')
        self.assertEqual(image.history[0],
                         'Created Image from {} as Test1'.format(path_to_tiff))

        # Without history...
        image = Image.from_file(path_to_tiff, log_in_history=False)
        self.assertEqual(len(image.history), 0)

        # It is worth noting the image can support more multiple channels.
        # This is particularly important when reading in images in rgb format.
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        image = Image.from_file(fpath)
        self.assertEqual(image.shape, (50, 50, 3))


    def test_16bit_tiff_file(self):
        from jicbioimage.core.image import Image
        im = Image.from_file(os.path.join(DATA_DIR, 'white-16bit.tiff'))
        self.assertEqual(im.dtype, np.uint16)
        self.assertEqual(np.max(im), np.iinfo(np.uint16).max)

    def test_repr_png_return_type(self):
        from jicbioimage.core.image import Image
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        image = Image.from_file(fpath)
        self.assertEqual(type(image._repr_png_()), bytes)

    def test_png_type(self):
        from jicbioimage.core.image import Image
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        image = Image.from_file(fpath)
        self.assertEqual(type(image.png()), bytes)

if __name__ == '__main__':
    unittest.main()
