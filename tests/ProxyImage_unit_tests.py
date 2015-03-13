"""Tests for the :class:`jicimagelib.image.ImageProxy` class."""

import unittest

class ImageProxyTests(unittest.TestCase):
    
    def test_instantiation(self):
        from jicimagelib.image import ImageProxy
        image_proxy = ImageProxy('dummy.tif', s=0, c=1, z=2, t=3)
        self.assertEqual(image_proxy.fpath, 'dummy.tif')
        self.assertEqual(image_proxy.series, 0)
        self.assertEqual(image_proxy.channel, 1)
        self.assertEqual(image_proxy.zslice, 2)
        self.assertEqual(image_proxy.timepoint, 3)

if __name__ == '__main__':
    unittest.main()
