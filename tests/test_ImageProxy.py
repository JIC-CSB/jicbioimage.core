"""Tests for the :class:`jicimagelib.image.ImageProxy` class."""

import unittest

class ImageProxyTests(unittest.TestCase):
    
    def test_instantiation(self):
        from jicimagelib.image import ImageProxy
        image_proxy = ImageProxy('dummy.tif')
        self.assertEqual(image_proxy.fpath, 'dummy.tif')
        
        
if __name__ == '__main__':
    unittest.main()
