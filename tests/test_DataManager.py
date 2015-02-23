"""Test the :class:`image.DataManager`."""

import unittest

class TestImports(unittest.TestCase):
    """Test importing modules and classes."""

    def test_import_image(self):
        """Test importing the image module."""
        # This throws an error if the module cannot be imported.
        from jicimagelib import image

    def test_import_DataManager(self):
        """Test importing the DataManager class."""
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import DataManager

    def test_import_BFConvertDataManager(self):
        """Test importing the BFConvertDataManager class."""
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import _BFConvertDataManager

class Test_BFConvertWrapper(unittest.TestCase):
    """Test the :class:`jicimagelib.image._BFConvertDataManager` class."""

    def test_split_order(self):
        """Test the split_order attribute."""
        from jicimagelib.image import _BFConvertDataManager
        bf_data_manager = _BFConvertDataManager()
        self.assertEqual(bf_data_manager.split_order, ['s', 'c', 'z', 't'])
        
    def test_split_pattern(self):
        """Test the split_pattern property."""
        from jicimagelib.image import _BFConvertDataManager
        bf_data_manager = _BFConvertDataManager()
        self.assertEqual(bf_data_manager.split_pattern, '_S%s_C%c_Z%z_T%t')
        bf_data_manager.split_order = ['z', 'c']
        self.assertEqual(bf_data_manager.split_pattern, '_Z%z_C%c')
        
    def test_run_command(self):
        """Test the run_command function."""
        from jicimagelib.image import _BFConvertDataManager
        bf_data_manager = _BFConvertDataManager()
        cmd = bf_data_manager.run_command('test.lif')
        self.assertEqual(cmd, 'bfconvert test.lif test_S%s_C%c_Z%z_T%t.tif')
        cmd = bf_data_manager.run_command('test.lif', output_dir='/tmp')
        self.assertEqual(cmd, 'bfconvert test.lif /tmp/test_S%s_C%c_Z%z_T%t.tif')

    def test_metadata_from_fname(self):
        """Test the metadata_from_fname function."""
        from jicimagelib.image import _BFConvertDataManager
        bf_data_manager = _BFConvertDataManager()
        meta_data = bf_data_manager.metadata_from_fname('test_S1_C2_Z3_T4.tif')
        self.assertEqual(meta_data.s, 1)
        self.assertEqual(meta_data.c, 2)
        self.assertEqual(meta_data.z, 3)
        self.assertEqual(meta_data.t, 4)



class TestDataManager(unittest.TestCase):
    """Test the :class:`jicimagelib.image.DataManager` class."""

