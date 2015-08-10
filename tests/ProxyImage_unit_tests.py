"""Tests for the :class:`jicimagelib.image.ProxyImage` class."""

import unittest

class ProxyImage(unittest.TestCase):
    
    def test_instantiation(self):
        from jicimagelib.image import ProxyImage
        proxy_image = ProxyImage('dummy.tif')
        self.assertEqual(proxy_image.fpath, 'dummy.tif')

    def test_repr(self):
        from jicimagelib.image import ProxyImage
        proxy_image = ProxyImage('dummy.tif')
        self.assertEqual(repr(proxy_image),
            '<ProxyImage object at {}>'.format(
                hex(id(proxy_image)))
        ) 

if __name__ == '__main__':
    unittest.main()

