"""Tests for the :class:`jicimagelib.image.ImageCollection` class."""

import unittest

class ImageCollectionTests(unittest.TestCase):
    
    def test_len(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertEqual(len(image_collection), 0)
        
    def test_has_image_proxy(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(callable(image_collection.image_proxy))

    def test_image_proxy(self):
        from jicimagelib.image import ImageCollection, ProxyImage
        image_collection = ImageCollection()
        image_collection.append(ProxyImage('test0.tif', s=0, c=0, z=0, t=0))
        image_collection.append(ProxyImage('test1.tif', s=1, c=1, z=1, t=1))

        image_proxy = image_collection.image_proxy()
        self.assertEqual(image_proxy.fpath, 'test0.tif')

        image_proxy = image_collection.image_proxy(s=1, c=1, z=1, t=1)
        self.assertEqual(image_proxy.fpath, 'test1.tif')

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
