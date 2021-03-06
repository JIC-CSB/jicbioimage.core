"""Tests for the :class:`jicbioimage.core.image.Image` class."""

import io

import unittest
import numpy as np

import PIL

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch


class BaseImageTests(unittest.TestCase):

    def test_repr(self):
        from jicbioimage.core.image import _BaseImage
        im = _BaseImage((50,50))
        pos = hex(id(im))
        expected = "<_BaseImage object at {}, dtype=float64>".format(pos)
        self.assertEqual(repr(im), expected)

        im = _BaseImage((50,50), dtype=bool)
        pos = hex(id(im))
        expected = "<_BaseImage object at {}, dtype=bool>".format(pos)
        self.assertEqual(repr(im), expected)

class ImageTests(unittest.TestCase):

    def test_repr(self):
        from jicbioimage.core.image import Image
        im = Image((50,50))
        pos = hex(id(im))
        expected = "<Image object at {}, dtype=uint8>".format(pos)
        self.assertEqual(repr(im), expected)

    def test_import_Image_class(self):
        # This throws an error if the class cannot be imported.
        from jicbioimage.core.image import Image

    def test_instantiation_from_shape(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50))
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertEqual(image.shape, (50, 50))
        self.assertEqual(len(image.history), 0)
        self.assertEqual(image.history.creation,
                         'Instantiated Image from shape (50, 50)')

    def test_instantiation_from_shape_no_history(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50), log_in_history=False)
        self.assertEqual(len(image.history), 0)


    def test_rgb_instantiation_from_shape(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50, 3))
        self.assertEqual(image.shape, (50, 50, 3))

    def test_default_type(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50))
        self.assertEqual(image.dtype, np.uint8,
            'Image type not np.uint8 but {}'.format(image.dtype))

    def test_default_name(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50))
        self.assertTrue(image.name is None)

    def test_instantiation_from_shape_with_name(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50), name='test')
        self.assertEqual(image.name, 'test')
        self.assertEqual(len(image.history), 0)
        self.assertEqual(image.history.creation,
                         'Instantiated Image from shape (50, 50) as test')

    def test_repr_png_callable(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50))
        self.assertTrue(callable(image._repr_png_))

    def test_png_attr(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50))
        self.assertTrue(hasattr(image, 'png'))

    def test_png(self):
        from jicbioimage.core.image import Image
        image = Image((600, 500), dtype=np.uint64)
        png = image.png()

        ar = np.asarray(PIL.Image.open(io.BytesIO(png)))

        self.assertEqual(ar.shape[0], 600)
        self.assertEqual(ar.shape[1], 500)

    def test_png_converts_to_uint8(self):
        from jicbioimage.core.image import Image
        image = Image((50, 50), dtype=np.uint64)
        # The below raises error if the image is not converted to uint8
        # before returning the png string.
        png = image.png

    def test_png_with_width(self):
        from jicbioimage.core.image import Image
        image = Image((600, 800), dtype=np.uint64)
        thumbnail = image.png(width=300)

        ar = np.asarray(PIL.Image.open(io.BytesIO(thumbnail)))

        self.assertEqual(ar.shape[0], 300)
        self.assertEqual(ar.shape[1], 400)

    def test_rgb_thumbnail(self):
        from jicbioimage.core.image import Image
        image = Image((600, 800, 3), dtype=np.uint64)
        thumbnail = image.png(width=300)

        ar = np.asarray(PIL.Image.open(io.BytesIO(thumbnail)))

        self.assertEqual(ar.shape[0], 300)
        self.assertEqual(ar.shape[1], 400)
        self.assertEqual(ar.shape[2], 3)


    def test_from_array(self):
        from jicbioimage.core.image import Image
        ar = np.zeros((50,50), dtype=np.uint8)
        im = Image.from_array(ar)
        self.assertTrue(isinstance(im, Image))
        self.assertEqual(len(im.history), 0)
        self.assertEqual(im.history.creation, 'Created Image from array')

    def test_from_array_with_name(self):
        from jicbioimage.core.image import Image
        ar = np.zeros((50,50), dtype=np.uint8)
        im = Image.from_array(ar, name='Test1')
        self.assertEqual(len(im.history), 0)
        self.assertEqual(im.history.creation, 'Created Image from array as Test1')

    def test_from_array_no_history(self):
        from jicbioimage.core.image import Image
        ar = np.zeros((50,50), dtype=np.uint8)
        im = Image.from_array(ar, log_in_history=False)
        self.assertEqual(len(im.history), 0)

class sorted_listdir_test(unittest.TestCase):

    @patch('os.listdir')
    def test_sorted_lisdir(self, patch_listdir):
        patch_listdir.return_value = ["z20.png", "z3.png", "z1.png"]
        from jicbioimage.core.image import _sorted_listdir
        l = _sorted_listdir(".")
        patch_listdir.assert_called_with(".")
        self.assertEqual(l, ["z1.png", "z3.png", "z20.png"])

if __name__ == '__main__':
    unittest.main()
