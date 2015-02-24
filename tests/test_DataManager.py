"""Test the :class:`image.DataManager`."""

import unittest
import os.path
import shutil

import numpy as np
from libtiff import TIFF

HERE = os.path.dirname(__file__)
TMPDIR = os.path.join(HERE, 'tmp')

def savetiff(fpath, ar):
    """Save a numpy array as a tiff file."""
    tif = TIFF.open(fpath, 'w')
    tif.write_image(ar)
    tif.close()
    

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

    def test_import_FileProxyImage(self):
        """Test importing the FileProxyImage class."""
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import _FileProxyImage

class Test_FileProxyImage(unittest.TestCase):
    """Test the :class:`jicimagelib.image._FileProxyImage` class."""

    def setUp(self):
        if not os.path.isdir(TMPDIR):
            os.mkdir(TMPDIR)
        self.tiff_fpath = os.path.join(TMPDIR, 'tmp.tiff')
        self.array = np.ones((50,50), dtype=np.uint8) 
        savetiff(self.tiff_fpath, self.array)

    def tearDown(self):
        shutil.rmtree(TMPDIR)

    def test_default_instantiation(self):
        """Test default instantiation of a _FileProxyImage."""
        from jicimagelib.image import _FileProxyImage
        proxy_image = _FileProxyImage('/tmp/image.tiff')
        self.assertEqual(proxy_image._fpath, '/tmp/image.tiff')
        self.assertEqual(proxy_image.series, None)
        self.assertEqual(proxy_image.channel, None)
        self.assertEqual(proxy_image.zslice, None)
        self.assertEqual(proxy_image.timepoint, None)

    def test_custom_instantiation(self):
        """Test default instantiation of a _FileProxyImage."""
        from jicimagelib.image import _FileProxyImage
        proxy_image = _FileProxyImage('/tmp/image.tiff', s=0, c=1, z=2, t=3)
        self.assertEqual(proxy_image._fpath, '/tmp/image.tiff')
        self.assertEqual(proxy_image.series, 0)
        self.assertEqual(proxy_image.channel, 1)
        self.assertEqual(proxy_image.zslice, 2)
        self.assertEqual(proxy_image.timepoint, 3)

    def test_image_property(self):
        """Test the image property."""
        from jicimagelib.image import _FileProxyImage
        proxy_image = _FileProxyImage(self.tiff_fpath)
        im = proxy_image.image
        self.assertEqual(im.dtype, self.array.dtype)
        self.assertEqual(im.shape, self.array.shape)

    

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

        bf_data_manager.split_order = ['z', 'c']
        meta_data = bf_data_manager.metadata_from_fname('test_Z3_C4.tif')
        self.assertEqual(meta_data.c, 4)
        self.assertEqual(meta_data.z, 3)



class TestDataManager(unittest.TestCase):
    """Test the :class:`jicimagelib.image.DataManager` class."""

