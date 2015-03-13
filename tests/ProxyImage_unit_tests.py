"""Tests for the :class:`jicimagelib.image.ProxyImage` class."""

import unittest

class ProxyImageTests(unittest.TestCase):
    
    def test_instantiation(self):
        from jicimagelib.image import ProxyImage
        proxy_image = ProxyImage('dummy.tif', s=0, c=1, z=2, t=3)
        self.assertEqual(proxy_image.fpath, 'dummy.tif')
        self.assertEqual(proxy_image.series, 0)
        self.assertEqual(proxy_image.channel, 1)
        self.assertEqual(proxy_image.zslice, 2)
        self.assertEqual(proxy_image.timepoint, 3)

if __name__ == '__main__':
    unittest.main()
