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
        self.assertEqual(image.history[0],
                         'Instantiated image from shape (50, 50)')
        
        
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
        self.assertEqual(image.history[0],
                         'Instantiated image from shape (50, 50) as test')
    
    def test_repr_png_callable(self):
        from jicimagelib.image import Image
        image = Image((50, 50))
        self.assertTrue(callable(image._repr_png_))
        
    def test_png_attr(self):
        from jicimagelib.image import Image
        image = Image((50, 50))
        self.assertTrue(hasattr(image, 'png'))
        
    def test_png_converts_to_uint8(self):
        from jicimagelib.image import Image
        image = Image((50, 50), dtype=np.uint64)
        # The below raises error if the image is not converted to uint8
        # before returning the png string.
        png = image.png

    def test_from_array(self):
        from jicimagelib.image import Image
        ar = np.zeros((50,50), dtype=np.uint8)
        im = Image.from_array(ar)
        self.assertTrue(isinstance(im, Image))
        self.assertEqual(im.history[0], 'Created image from array')

    def test_from_array_with_name(self):
        from jicimagelib.image import Image
        ar = np.zeros((50,50), dtype=np.uint8)
        im = Image.from_array(ar, name='Test1')
        self.assertEqual(im.history[0], 'Created image from array as Test1')


        
if __name__ == '__main__':
    unittest.main()
