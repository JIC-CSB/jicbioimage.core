"""Tests for the :class:`jicimagelib.image.DataManager` class."""

import unittest

class DataManagerTests(unittest.TestCase):
    
    def test_load_function_exists(self):
        from jicimagelib.image import DataManager
        data_manager = DataManager()
        self.assertTrue(callable(data_manager.load))
        
if __name__ == '__main__':
    unittest.main()
