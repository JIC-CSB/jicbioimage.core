"""Tests for the :class:`jicimagelib.image.DataManager` class."""

import unittest

class DataManagerTests(unittest.TestCase):
    
    def test_load_function_exists(self):
        from jicimagelib.image import DataManager
        data_manager = DataManager('dummy')
        self.assertTrue(callable(data_manager.load))
        
    def test_default_backend(self):
        from jicimagelib.image import DataManager, FileBackend
        backend = FileBackend('dummy')
        data_manager = DataManager(backend)
        self.assertTrue(isinstance(data_manager.backend, FileBackend))
         
    def test_default_convert(self):
        from jicimagelib.image import DataManager, _BFConvertWrapper
        data_manager = DataManager('dummy')
        self.assertTrue(isinstance(data_manager.convert, _BFConvertWrapper))
         

if __name__ == '__main__':
    unittest.main()
