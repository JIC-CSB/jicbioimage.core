"""Functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np

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

    def test_data_manager_already_unpacked(self):
        # The second time the data manager is loaded, it should contain data
        # without unpacking.

        from jicimagelib.image import DataManager, FileBackend

        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)

        data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        self.assertEqual(len(data_manager), 1)

        backend_reload = FileBackend(TMP_DIR)
        data_manager_reload = DataManager(backend)

        data_manager_reload.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        self.assertEqual(len(data_manager_reload), 1)

    def test_error_message_when_bfconvert_not_in_path(self):
        from jicimagelib.image import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        tmp_path = os.environ['PATH']
        del os.environ['PATH']
        with self.assertRaises(RuntimeError):
            data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        os.environ['PATH'] = tmp_path

    def test_image_proxy(self):
        from jicimagelib.image import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        data_manager.load(os.path.join(DATA_DIR, 'single-channel.ome.tif'))
        image_collection = data_manager[0]
        image_proxy = image_collection.image_proxy()
        self.assertTrue(os.path.isfile(image_proxy.fpath),
                        'no such file: {}'.format(image_proxy.fpath))
        self.assertTrue(isinstance(image_proxy.image, np.ndarray))
        self.assertEqual(image_proxy.image.shape, (167, 439))

    def test_image_collection(self):
        from jicimagelib.image import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)
        data_manager.load(os.path.join(DATA_DIR, 'multi-channel-4D-series.ome.tif'))
        image_collection = data_manager[0]
        self.assertEqual(len(image_collection), 7*5*3) # 7t, 5z, 3c

        image_proxy = image_collection.image_proxy()
        self.assertEqual(image_proxy.series, 0)
        self.assertEqual(image_proxy.channel, 0)
        self.assertEqual(image_proxy.zslice, 0)
        self.assertEqual(image_proxy.timepoint, 0)

        image_proxy = image_collection.image_proxy(s=0, c=1, z=2, t=3)
        self.assertEqual(image_proxy.series, 0)
        self.assertEqual(image_proxy.channel, 1)
        self.assertEqual(image_proxy.zslice, 2)
        self.assertEqual(image_proxy.timepoint, 3)

        self.assertEqual(5,
            len([i for i in image_collection.zstack_proxy_iterator()]))
        for i, image_proxy in enumerate(image_collection.zstack_proxy_iterator()):
            self.assertEqual(image_proxy.series, 0)
            self.assertEqual(image_proxy.channel, 0)
            self.assertEqual(image_proxy.zslice, i)
            self.assertEqual(image_proxy.timepoint, 0)

        self.assertEqual(5,
            len([i for i in image_collection.zstack_proxy_iterator(s=0, c=1, t=3)]))
        for i, image_proxy in enumerate(image_collection.zstack_proxy_iterator(s=0, c=1, t=3)):
            self.assertEqual(image_proxy.series, 0)
            self.assertEqual(image_proxy.channel, 1)
            self.assertEqual(image_proxy.zslice, i)
            self.assertEqual(image_proxy.timepoint, 3)

        zstack_array = image_collection.zstack_array(s=0, c=1, t=3)
        self.assertTrue(isinstance(zstack_array, np.ndarray))
        self.assertEqual(zstack_array.shape, (167, 439, 5))

        image = image_collection.image(s=0, c=1, z=2, t=3)
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertEqual(image.shape, (167, 439))

class ImageUserStory(unittest.TestCase):
    
    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_manual_image_creation(self):

        from jicimagelib.image import Image

        # Preamble: let us define the path to a TIFF file and create a numpy
        # array from it.
        from libtiff import TIFF
        path_to_tiff = os.path.join(DATA_DIR, 'single-channel.ome.tif')
        tif = TIFF.open(path_to_tiff, 'r')
        ar = tif.read_image()

        # An image is just a subclass of a numpy.ndarray, so we can instantiate
        # it as such.
        image = Image((50, 50))
        self.assertTrue(isinstance(image, np.ndarray))

        # However, unlike a numpy.ndarray our image has a history associated
        # with it.
        self.assertEqual(image.history[0],
                         'Instantiated image from shape (50, 50)')

        # Optionally, we can also give our image a name.
        image = Image((50, 50), name='Test1')
        self.assertEqual(image.history[0],
                         'Instantiated image from shape (50, 50) as Test1')
        

        # It is also possible to create an image from an array.
        image = Image.from_array(ar)
        self.assertEqual(image.history[0],
                         'Created image from array')
        image = Image.from_array(ar, name='Test1')
        self.assertEqual(image.history[0],
                         'Created image from array as Test1')

        # It is also possible to create an image from a file.
        image = Image.from_file(path_to_tiff, format='tiff')
        self.assertEqual(image.history[0],
                         'Created image from {}'.format(path_to_tiff))

        # File format from file name.
        image = Image.from_file(path_to_tiff, name='Test1')
        self.assertEqual(image.history[0],
                         'Created image from {} as Test1'.format(path_to_tiff))

        # It is worth noting the image can support more multiple channels.
        image = Image((50, 50, 3))

        # This is particularly important when reading in images in rgb format.
        fpath = os.path.join(DATA_DIR, 'tjelvar.png')
        image = Image.from_file(fpath, format="png")
        self.assertEqual(image.shape, (50, 50, 3))
        
        
    def test_unknown_file_format_raises_runtime_error(self):
        from jicimagelib.image import Image
        with self.assertRaises(RuntimeError):
            im = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'),
                                 format='unknown')
        
    def test_can_deal_with_upper_case_file_format(self):
        from jicimagelib.image import Image
        im = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'),
                             format='PNG')

class TransformationUserStory(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)


    def test_creating_transformations_from_scratch(self):
        
        # What if the default names of images was just the order in which they
        # were created?
        # Or perhaps the order + the function name, e.g.
        # 1_gaussian.png
        # 2_sobel.png
        # 3_gaussian.png
        # The order could be tracked in a class variable in an AutoName
        # object. The AutoName object could also store the output directory
        # as a class variable.

        # One could also have class named AutoWrite with a class variable
        # ``on``, which is True by default.


        # AutoSave
        from jicimagelib.io import AutoWrite
        self.assertTrue(AutoWrite.on)

        AutoName.directory = TMP_DIR
        self.assertEqual(AutoName.name(my_func),
                         os.path.join(TMP_DIR, '2_no_transform.png'))


        from jicimagelib.transform import transformation

        @transformation
        def identity(image):
            return image

        image = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))
        image = identity(image)
        self.assertEqual(repr(image.history[-1]), 'Applied identity transform')
        created_fpath = os.path.join(AutoName.directory, '3_identity.png')
        self.assertTrue(os.path.isfile(created_fpath))



if __name__ == '__main__':
    unittest.main()
