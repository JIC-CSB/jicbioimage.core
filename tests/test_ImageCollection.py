"""Tests for the :class:`jicimagelib.image.ImageCollection` class."""

import unittest

class ImageCollectionTests(unittest.TestCase):
    
    def test_len(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertEqual(len(image_collection), 0)

    def test_add_image(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        image_collection.add_image_proxy('dummy')
        
        
if __name__ == '__main__':
    unittest.main()
