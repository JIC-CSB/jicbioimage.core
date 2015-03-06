"""Tests for the :class:`jicimagelib.image.Image` class."""

import unittest
import numpy as np

class ImageTests(unittest.TestCase):

    def test_import_Image_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import Image
        
    def test_instantiation_from_shape(self):
        from jicimagelib.image import Image
        image = Image((50, 50))
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertEqual(image.shape, (50, 50))
        
    def test_rgb_instantiation_from_shape(self):
        from jicimagelib.image import Image
        image = Image((50, 50, 3))
        self.assertEqual(image.shape, (50, 50, 3))

    def test_default_type(self):
        from jicimagelib.image import Image
        image = Image((50, 50))
        self.assertEqual(image.dtype, np.uint8,
            'Image type not np.uint8 but {}'.format(image.dtype))

    def test_default_name(self):
        from jicimagelib.image import Image
        image = Image((50, 50))
        self.assertTrue(image.name is None)
        
    def test_instantiation_from_shape_with_name(self):
        from jicimagelib.image import Image
        image = Image((50, 50), name='test')
        self.assertEqual(image.name, 'test')
    
if __name__ == '__main__':
    unittest.main()
