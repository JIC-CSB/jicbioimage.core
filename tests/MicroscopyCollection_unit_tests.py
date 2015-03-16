"""Tests for the :class:`jicimagelib.image.MicroscopyCollection` class."""

import unittest

class MicroscopyCollectionTests(unittest.TestCase):
    
    def test_len(self):
        from jicimagelib.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertEqual(len(microscopy_collection), 0)
        
    def test_has_proxy_image(self):
        from jicimagelib.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.proxy_image))

    def test_proxy_image(self):
        from jicimagelib.image import MicroscopyCollection, MicroscopyImage
        microscopy_collection = MicroscopyCollection()
        microscopy_collection.append(MicroscopyImage('test0.tif',
            dict(series=0, channel=0, zslice=0, timepoint=0)))
        microscopy_collection.append(MicroscopyImage('test1.tif',
            dict(series=1, channel=1, zslice=1, timepoint=1)))

        proxy_image = microscopy_collection.proxy_image()
        self.assertEqual(proxy_image.fpath, 'test0.tif')

        proxy_image = microscopy_collection.proxy_image(s=1, c=1, z=1, t=1)
        self.assertEqual(proxy_image.fpath, 'test1.tif')

    def test_zstack_proxy_iterator(self):
        from jicimagelib.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.zstack_proxy_iterator))
        
    def test_zstack_proxy_iterator_is_iterable(self):
        import collections
        from jicimagelib.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(isinstance(microscopy_collection.zstack_proxy_iterator(),
                                   collections.Iterable))
        self.assertTrue(isinstance(microscopy_collection.zstack_proxy_iterator(),
                                   collections.Iterable))
        
    def test_zstack_array(self):
        from jicimagelib.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.zstack_array))
        
    def test_zstack_array(self):
        from jicimagelib.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.image))
        
if __name__ == '__main__':
    unittest.main()
