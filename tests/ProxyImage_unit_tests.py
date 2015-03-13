"""Tests for the :class:`jicimagelib.image.ProxyImage` class."""

import unittest

class ProxyImage(unittest.TestCase):
    
    def test_instantiation(self):
        from jicimagelib.image import ProxyImage
        proxy_image = ProxyImage('dummy.tif')
        self.assertEqual(proxy_image.fpath, 'dummy.tif')

if __name__ == '__main__':
    unittest.main()

