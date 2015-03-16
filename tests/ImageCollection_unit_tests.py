"""Tests for the :class:`jicimagelib.image.ImageCollection` class."""

import unittest

class ImageCollectionTests(unittest.TestCase):
    
    def test_len(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertEqual(len(image_collection), 0)
        
    def test_has_proxy_image(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(callable(image_collection.proxy_image))

    def test_proxy_image(self):
        from jicimagelib.image import ImageCollection, ProxyImage
        image_collection = ImageCollection()
        image_collection.append(ProxyImage('test0.tif'))
        image_collection.append(ProxyImage('test1.tif'))

        proxy_image = image_collection.proxy_image()
        self.assertEqual(proxy_image.fpath, 'test0.tif')

        proxy_image = image_collection.proxy_image(index=1)
        self.assertEqual(proxy_image.fpath, 'test1.tif')

if __name__ == '__main__':
    unittest.main()

