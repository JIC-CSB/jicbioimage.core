"""Functional tests."""

import unittest
import os
import os.path
import shutil

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')

class DataManagerUserStory(unittest.TestCase):
    
    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_data_manager(self):
        # Alice wants to analyse her microscopy data.  To access the raw image
        # data within the microscopy files she uses a DataManager.
        from jicimagelib.image import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)

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

        # Alice then loads her second file of interest.
        data_manager.load(os.path.join(DATA_DIR, 'z-series.ome.tif'))

        # The data manager now contains to image collections.
        self.assertEqual(len(data_manager), 2)

        # There are five z-slices in the new image collection.
        zseries_collection = data_manager[1]
        self.assertEqual(len(zseries_collection), 5)
 
        # File format conversion trouble (for example using non existing input
        # file) raises RuntimeError.
        with self.assertRaises(RuntimeError):
            data_manager.load(os.path.join(DATA_DIR, 'nonsese.ome.tif'))



if __name__ == '__main__':
    unittest.main()
