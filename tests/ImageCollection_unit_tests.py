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
        image_collection.append(ProxyImage('test0.tif', s=0, c=0, z=0, t=0))
        image_collection.append(ProxyImage('test1.tif', s=1, c=1, z=1, t=1))

        proxy_image = image_collection.proxy_image()
        self.assertEqual(proxy_image.fpath, 'test0.tif')

        proxy_image = image_collection.proxy_image(s=1, c=1, z=1, t=1)
        self.assertEqual(proxy_image.fpath, 'test1.tif')

    def test_zstack_proxy_iterator(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(callable(image_collection.zstack_proxy_iterator))
        
    def test_zstack_proxy_iterator_is_iterable(self):
        import collections
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(isinstance(image_collection.zstack_proxy_iterator(),
                                   collections.Iterable))
        self.assertTrue(isinstance(image_collection.zstack_proxy_iterator(),
                                   collections.Iterable))
        
    def test_zstack_array(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(callable(image_collection.zstack_array))
        
    def test_zstack_array(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(callable(image_collection.image))
        
if __name__ == '__main__':
    unittest.main()
