"""Tests for the :class:`jicbioimage.core.image.Image3D class."""

import unittest
import numpy as np

class Image3D_unit_tests(unittest.TestCase):

    def test_import_Image3D_class(self):
        # This throws an error if the class cannot be imported.
        from jicbioimage.core.image import Image3D

    def test_instantiation_from_shape(self):
        from jicbioimage.core.image import Image3D
        image = Image3D((50, 50, 50))
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertEqual(image.shape, (50, 50, 50))
        self.assertEqual(image.history[0],
                         'Instantiated Image3D from shape (50, 50, 50)')

    def test_instantiation_from_shape_no_history(self):
        from jicbioimage.core.image import Image3D
        image = Image3D((50, 50, 50), log_in_history=False)
        self.assertEqual(len(image.history), 0)

    def test_default_type(self):
        from jicbioimage.core.image import Image3D
        image = Image3D((50, 50, 50))
        self.assertEqual(image.dtype, np.uint8,
            'Image type not np.uint8 but {}'.format(image.dtype))

    def test_default_name(self):
        from jicbioimage.core.image import Image3D
        image = Image3D((50, 50, 50))
        self.assertTrue(image.name is None)

    def test_instantiation_from_shape_with_name(self):
        from jicbioimage.core.image import Image3D
        image = Image3D((50, 50, 50), name='test')
        self.assertEqual(image.name, 'test')
        self.assertEqual(image.history[0],
                         'Instantiated Image3D from shape (50, 50, 50) as test')

    def test_from_array(self):
        from jicbioimage.core.image import Image3D
        ar = np.zeros((50,50,50), dtype=np.uint8)
        im = Image3D.from_array(ar)
        self.assertTrue(isinstance(im, Image3D))
        self.assertEqual(im.history[0], 'Created Image3D from array')

    def test_from_array_with_name(self):
        from jicbioimage.core.image import Image3D
        ar = np.zeros((50,50,50), dtype=np.uint8)
        im = Image3D.from_array(ar, name='Test1')
        self.assertEqual(im.history[0], 'Created Image3D from array as Test1')

    def test_from_array_no_history(self):
        from jicbioimage.core.image import Image3D
        ar = np.zeros((50,50,50), dtype=np.uint8)
        im = Image3D.from_array(ar, log_in_history=False)
        self.assertEqual(len(im.history), 0)

    def test_num_digits(self):
        from jicbioimage.core.image import Image3D
        self.assertEqual(Image3D._num_digits(1), 1)
        self.assertEqual(Image3D._num_digits(9), 1)
        self.assertEqual(Image3D._num_digits(10), 2)
        self.assertEqual(Image3D._num_digits(99), 2)
        self.assertEqual(Image3D._num_digits(100), 3)
