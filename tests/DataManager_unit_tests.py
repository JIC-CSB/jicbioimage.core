"""Tests for the :class:`jicimagelib.image.DataManager` class."""

import unittest
import os
import os.path
import shutil

HERE = os.path.dirname(__file__)
TMP_DIR = os.path.join(HERE, 'tmp')

class DataManagerTests(unittest.TestCase):
    
    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_load_function_exists(self):
        from jicimagelib.image import DataManager
        data_manager = DataManager(os.path.join(TMP_DIR, 'dummy'))
        self.assertTrue(callable(data_manager.load))
        
    def test_backend(self):
        from jicimagelib.image import DataManager
        from jicimagelib.io import FileBackend
        backend = FileBackend(os.path.join(TMP_DIR, 'dummy'))
        data_manager = DataManager(backend)
        self.assertTrue(isinstance(data_manager.backend, FileBackend))
         
    def test_default_convert(self):
        from jicimagelib.image import DataManager, BFConvertWrapper
        data_manager = DataManager(os.path.join(TMP_DIR, 'dummy'))
        self.assertTrue(isinstance(data_manager.convert, BFConvertWrapper))
         

if __name__ == '__main__':
    unittest.main()
