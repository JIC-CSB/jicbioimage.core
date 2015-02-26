"""Functional tests for the data manager."""


import unittest
import os
import os.path
import shutil

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class TestDataManager(unittest.TestCase):
    
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

if __name__ == '__main__':
    unittest.main()
