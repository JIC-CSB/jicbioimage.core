"""DataManager functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np
from skimage.io import imread, use_plugin

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
        # We start off by creating a :class:`jicbioimage.core.io.DataManager`.
        # This takes a backend argument. The backend provides a means to store
        # unpacked image files.
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(directory=TMP_DIR)
        data_manager = DataManager(backend=backend)

        # The :func:`jicbioimage.core.image.DataManager.conver` function is be
        # default an instance of the callable
        # :class:`jicbioimage.core.io.BFConvertWrapper` class.
        from jicbioimage.core.io import BFConvertWrapper, _md5_hexdigest_from_file
        self.assertTrue(isinstance(data_manager.convert, BFConvertWrapper))

        # We also need to import an ImageCollection
        from jicbioimage.core.image import ImageCollection

        # If the input file has not already been converted with do so.
        fpath = os.path.join(DATA_DIR, 'z-series.ome.tif')
        self.assertFalse(data_manager.convert.already_converted(fpath))
        if not data_manager.convert.already_converted(fpath):
            path_to_manifest = data_manager.convert(fpath) # unpacks and creates manifests
            self.assertEqual(path_to_manifest, os.path.join(TMP_DIR,
                                                            _md5_hexdigest_from_file(fpath),
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
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)

        # Initially the DataManger is empty.
        self.assertEqual(len(data_manager), 0)

        # Alice loads her file of interest.
        data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        self.assertEqual(len(data_manager), 1)
        
        # A DataManager is a container for MicroscopyCollection instances.
        from jicbioimage.core.image import MicroscopyCollection
        microscopy_collection = data_manager[0]
        self.assertTrue(isinstance(microscopy_collection, MicroscopyCollection))

        # In this instance the image collection only contains one item.
        self.assertEqual(len(microscopy_collection), 1)
        image = microscopy_collection[0]

        # A MicroscopyCollection is a container for MicroscopyImage instances.
        from jicbioimage.core.image import MicroscopyImage
        self.assertTrue(isinstance(image, MicroscopyImage))

        # Alice then loads her second file of interest.
        data_manager.load(os.path.join(DATA_DIR, 'z-series.ome.tif'))

        # The data manager now contains to image collections.
        self.assertEqual(len(data_manager), 2)

        # There are five z-slices in the new image collection.
        zseries_collection = data_manager[1]
        self.assertEqual(len(zseries_collection), 5)
 
        # File format conversion trouble (for example using non existing input
        # file) raises IOError.
        with self.assertRaises(IOError):
            data_manager.load(os.path.join(DATA_DIR, 'nonsese.ome.tif'))

    def test_data_manager_already_unpacked(self):
        # The second time the data manager is loaded, it should contain data
        # without unpacking.

        from jicbioimage.core.io import DataManager, FileBackend

        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)

        data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        self.assertEqual(len(data_manager), 1)

        backend_reload = FileBackend(TMP_DIR)
        data_manager_reload = DataManager(backend)

        data_manager_reload.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        self.assertEqual(len(data_manager_reload), 1)

    def test_error_message_when_bfconvert_not_in_path(self):
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        tmp_path = os.environ['PATH']
        del os.environ['PATH']
        with self.assertRaises(RuntimeError):
            data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        os.environ['PATH'] = tmp_path

    def test_proxy_image(self):
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        microscopy_collection = data_manager[0]
        proxy_image = microscopy_collection.proxy_image()
        self.assertTrue(os.path.isfile(proxy_image.fpath),
                        'no such file: {}'.format(proxy_image.fpath))
        self.assertTrue(isinstance(proxy_image.image, np.ndarray))
        self.assertEqual(proxy_image.image.shape, (167, 439))

    def test_image_collection(self):
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        data_manager.load(os.path.join(DATA_DIR, 'multi-channel-4D-series.ome.tif'))
        microscopy_collection = data_manager[0]
        self.assertEqual(len(microscopy_collection), 7*5*3) # 7t, 5z, 3c

        proxy_image = microscopy_collection.proxy_image()
        self.assertEqual(proxy_image.series, 0)
        self.assertEqual(proxy_image.channel, 0)
        self.assertEqual(proxy_image.zslice, 0)
        self.assertEqual(proxy_image.timepoint, 0)

        proxy_image = microscopy_collection.proxy_image(s=0, c=1, z=2, t=3)
        self.assertEqual(proxy_image.series, 0)
        self.assertEqual(proxy_image.channel, 1)
        self.assertEqual(proxy_image.zslice, 2)
        self.assertEqual(proxy_image.timepoint, 3)

        self.assertEqual(5,
            len([i for i in microscopy_collection.zstack_proxy_iterator()]))
        for i, proxy_image in enumerate(microscopy_collection.zstack_proxy_iterator()):
            self.assertEqual(proxy_image.series, 0)
            self.assertEqual(proxy_image.channel, 0)
            self.assertEqual(proxy_image.zslice, i)
            self.assertEqual(proxy_image.timepoint, 0)

        self.assertEqual(5,
            len([i for i in microscopy_collection.zstack_proxy_iterator(s=0, c=1, t=3)]))
        for i, proxy_image in enumerate(microscopy_collection.zstack_proxy_iterator(s=0, c=1, t=3)):
            self.assertEqual(proxy_image.series, 0)
            self.assertEqual(proxy_image.channel, 1)
            self.assertEqual(proxy_image.zslice, i)
            self.assertEqual(proxy_image.timepoint, 3)

        zstack_array = microscopy_collection.zstack_array(s=0, c=1, t=3)
        self.assertTrue(isinstance(zstack_array, np.ndarray))
        self.assertEqual(zstack_array.shape, (167, 439, 5))

        image = microscopy_collection.image(s=0, c=1, z=2, t=3)
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertEqual(image.shape, (167, 439))
         
    def test_multipage_tiff(self):
        from jicbioimage.core.image import MicroscopyCollection, ImageCollection
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(directory=TMP_DIR)
        data_manager = DataManager(backend)
        data_manager.load(os.path.join(DATA_DIR, 'multipage.tif'))
        image_collection = data_manager[0]

        # When we load a multipage tiff file we get an ImageCollection not a
        # MicroscopyCollection.
        self.assertFalse(isinstance(image_collection, MicroscopyCollection))
        self.assertTrue(isinstance(image_collection, ImageCollection))

        # Let us get the first proxy image.
        first_proxy_image = image_collection.proxy_image()
        self.assertTrue(os.path.isfile(first_proxy_image.fpath))

        # Let us get the last proxy image.
        last_proxy_image = image_collection.proxy_image(index=-1)
        self.assertTrue(os.path.isfile(last_proxy_image.fpath))

        # Let us get some actual images.
        first_image = image_collection.image()
        self.assertEqual(np.max(first_image), 30)
        second_image = image_collection.image(1)
        self.assertEqual(np.max(second_image), 90)
        third_image = image_collection.image(index=2)
        self.assertEqual(np.max(third_image), 120)

    def test_load_returns_collection(self):
        from jicbioimage.core.image import ImageCollection
        from jicbioimage.core.image import MicroscopyImage, ProxyImage
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(directory=TMP_DIR)
        data_manager = DataManager(backend)
        collection = data_manager.load(os.path.join(DATA_DIR, 'multipage.tif'))
        self.assertTrue(isinstance(collection, ImageCollection))
        self.assertFalse(isinstance(collection[0], MicroscopyImage))
        self.assertTrue(isinstance(collection[0], ProxyImage))

    def test_initialisation_without_explicit_backend(self):
        from jicbioimage.core.io import DataManager

        real_working_dir = os.getcwd()

        try:
            os.chdir(TMP_DIR)
            data_manager = DataManager()
            
            file_backend_path = os.path.join(os.getcwd(), 'jicbioimage.core_backend')

            self.assertEqual(data_manager.backend.directory, file_backend_path)
        finally:
            os.chdir(real_working_dir)
        
if __name__ == '__main__':
    unittest.main()
