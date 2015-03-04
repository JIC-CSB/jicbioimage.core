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

    def test_manual_addition_of_ImageCollection_to_DataManager(self):
        # We start off by creating a :class:`jicimagelib.image.DataManager`.
        # This takes a backend argument. The backend provides a means to store
        # unpacked image files.
        from jicimagelib.image import FileBackend
        from jicimagelib.image import DataManager
        backend = FileBackend(directory=TMP_DIR)
        data_manager = DataManager(backend=backend)

        # The :func:`jicimagelib.image.DataManager.conver` function is be
        # default an instance of the callable
        # :class:`jicimagelib.image._BFConvertWrapper` class.
        from jicimagelib.image import _BFConvertWrapper
        self.assertTrue(isinstance(data_manager.convert, _BFConvertWrapper))

        # We also need to import an ImageCollection
        from jicimagelib.image import ImageCollection

        # If the input file has not already been converted with do so.
        fpath = os.path.join(DATA_DIR, 'z-series.ome.tif')
        self.assertFalse(data_manager.convert.already_converted(fpath))
        if not data_manager.convert.already_converted(fpath):
            path_to_manifest = data_manager.convert(fpath) # unpacks and creates manifests
            self.assertEqual(path_to_manifest, os.path.join(TMP_DIR,
                                                            'z-series.ome.tif',
                                                            'manifest.json'))
            image_collection = ImageCollection()
            image_collection.parse_manifest(path_to_manifest)
            self.assertEqual(len(image_collection), 5)
            data_manager.append(image_collection)
            self.assertEqual(len(data_manager), 1)
        self.assertTrue(data_manager.convert.already_converted(fpath))

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

    def test_error_message_when_bfconvert_not_in_path(self):
        from jicimagelib.image import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        tmp_path = os.environ['PATH']
        del os.environ['PATH']
        with self.assertRaises(RuntimeError):
            data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        os.environ['PATH'] = tmp_path

    def test_image_collection(self):
        from jicimagelib.image import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        data_manager.load(os.path.join(DATA_DIR, 'multi-channel-4D-series.ome.tif'))
        image_collection = data_manager[0]
        self.assertEqual(len(image_collection), 7*5*3) # 7t, 5z, 3c

        image_proxy = image_collection.get_image_proxy()
        self.assertEqual(image_proxy.series, 0)
        self.assertEqual(image_proxy.channel, 0)
        self.assertEqual(image_proxy.zslice, 0)
        self.assertEqual(image_proxy.timepoint, 0)

        image_proxy = image_collection.get_image_proxy(s=0, c=1, z=2, t=3)
        self.assertEqual(image_proxy.series, 0)
        self.assertEqual(image_proxy.channel, 1)
        self.assertEqual(image_proxy.zslice, 2)
        self.assertEqual(image_proxy.timepoint, 3)

        self.assertEqual(5,
            len([i for i in image_collection.get_zstack_iterator()]))
        for i, image_proxy in enumerate(image_collection.get_zstack_iterator()):
            self.assertEqual(image_proxy.series, 0)
            self.assertEqual(image_proxy.channel, 0)
            self.assertEqual(image_proxy.zslice, i)
            self.assertEqual(image_proxy.timepoint, 0)

        self.assertEqual(5,
            len([i for i in image_collection.get_zstack_iterator(s=0, c=1, t=3)]))
        for i, image_proxy in enumerate(image_collection.get_zstack_iterator(s=0, c=1, t=3)):
            self.assertEqual(image_proxy.series, 0)
            self.assertEqual(image_proxy.channel, 1)
            self.assertEqual(image_proxy.zslice, i)
            self.assertEqual(image_proxy.timepoint, 3)

        zstack_array = image_collection.get_zstack_array(s=0, c=1, t=3)
        import numpy as np
        self.assertTrue(isinstance(zstack_array, np.ndarray))
        self.assertEqual(zstack_array.shape, (50, 250, 5))

        image = image_collection.get_image(s=0, c=1, z=2, t=3)
        self.assertTrue(isinstance(zstack_array, np.ndarray))
        self.assertEqual(zstack_array.shape, (50, 250))

if __name__ == '__main__':
    unittest.main()
