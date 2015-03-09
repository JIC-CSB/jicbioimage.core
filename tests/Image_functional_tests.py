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

    def test_manual_image_creation(self):

        from jicimagelib.image import Image

        # Preamble: let us define the path to a TIFF file and create a numpy
        # array from it.
#       from libtiff import TIFF
#       tif = TIFF.open(path_to_tiff, 'r')
#       ar = tif.read_image()
        path_to_tiff = os.path.join(DATA_DIR, 'single-channel.ome.tif')
        use_plugin('freeimage')
        ar = imread(path_to_tiff)

        # An image is just a subclass of a numpy.ndarray, so we can instantiate
        # it as such.
        image = Image((50, 50))
        self.assertTrue(isinstance(image, np.ndarray))

        # However, unlike a numpy.ndarray our image has a history associated
        # with it.
        self.assertEqual(image.history[0],
                         'Instantiated image from shape (50, 50)')

        # Optionally, we can also give our image a name.
        image = Image((50, 50), name='Test1')
        self.assertEqual(image.history[0],
                         'Instantiated image from shape (50, 50) as Test1')
        

        # It is also possible to create an image from an array.
        image = Image.from_array(ar)
        self.assertEqual(image.history[0],
                         'Created image from array')
        image = Image.from_array(ar, name='Test1')
        self.assertEqual(image.history[0],
                         'Created image from array as Test1')

        # It is also possible to create an image from a file.
        image = Image.from_file(path_to_tiff, format='tiff')
        self.assertEqual(image.history[0],
                         'Created image from {}'.format(path_to_tiff))

        # File format from file name.
        image = Image.from_file(path_to_tiff, name='Test1')
        self.assertEqual(image.history[0],
                         'Created image from {} as Test1'.format(path_to_tiff))

        # It is worth noting the image can support more multiple channels.
        image = Image((50, 50, 3))

        # This is particularly important when reading in images in rgb format.
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        image = Image.from_file(fpath, format="png")
        self.assertEqual(image.shape, (50, 50, 3))
        
        
    def test_16bit_tiff_file(self):
        from jicimagelib.image import Image
        im = Image.from_file(os.path.join(DATA_DIR, 'white-16bit.tiff'))
        self.assertEqual(im.dtype, np.uint16)
        self.assertEqual(np.max(im), np.iinfo(np.uint16).max)

    def test_repr_png_return_type(self):
        from jicimagelib.image import Image
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        image = Image.from_file(fpath, format="png")
        self.assertEqual(type(image._repr_png_()), bytes)
        
if __name__ == '__main__':
    unittest.main()
