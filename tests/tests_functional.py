"""Functional tests."""

import unittest
import os.path

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')

class DataManagerUserStory(unittest.TestCase):
    
    def test_data_manager(self):
        # Alice wants to analyse her microscopy data.  To access the raw image
        # data within the microscopy files she uses a DataManager.
        from jicimagelib.image import DataManager
        data_manager = DataManager()

        # Initially the DataManger is empty.
        self.assertEqual(len(data_manager), 0)

        # Alice loads her file of interest.
        data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        self.assertEqual(len(data_manager), 1)
        
        # A DataManager is a container for ImageCollections.
        from jicimagelib.image import ImageCollection
        image_collection = data_manager[0]
        self.assertTrue(isinstance(image_collection, ImageCollection))

        # In this instance the image collection only contains one item.
        self.assertEqual(len(image_collection), 1)
        image = image_collection[0]

        # An ImageCollection is a container for ImageProxy instances.
        from jicimagelib.image import ImageProxy
        self.assertTrue(isinstance(image, ImageProxy))



if __name__ == '__main__':
    unittest.main()
