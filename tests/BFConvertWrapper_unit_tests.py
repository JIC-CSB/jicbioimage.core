"""Tests for the :class:`jicbioimage.core.image.BFConvertWrapper` class."""

import unittest
import os.path

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

HERE = os.path.dirname(__file__)

class BFConvertWrapperTests(unittest.TestCase):
    
    def test_backend_attribute(self):
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        self.assertEqual(wrapper.backend, 'backend')

    def test_split_order(self):
        """Test the split_order attribute."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        self.assertEqual(wrapper.split_order, ['s', 'c', 'z', 't'])

    def test_split_pattern(self):
        """Test the split_pattern property."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        self.assertEqual(wrapper.split_pattern, '_S%s_C%c_Z%z_T%t')
        wrapper.split_order = ['z', 'c']
        self.assertEqual(wrapper.split_pattern, '_Z%z_C%c')

    def test_run_command(self):
        """Test the run_command function."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        cmd = wrapper.run_command('test.lif')
        self.assertEqual(cmd, ['bfconvert',
                               'test.lif',
                               'test_S%s_C%c_Z%z_T%t.tif'])
        cmd = wrapper.run_command('test.lif', output_dir='/tmp')
        self.assertEqual(cmd, ['bfconvert',
                               'test.lif',
                               '/tmp/test_S%s_C%c_Z%z_T%t.tif'])

    def test_metadata_from_fname(self):
        """Test the metadata_from_fname function."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')

        meta_data = wrapper.metadata_from_fname('test_S1_C2_Z3_T4.tif')
        self.assertEqual(meta_data.s, 1)
        self.assertEqual(meta_data.c, 2)
        self.assertEqual(meta_data.z, 3)
        self.assertEqual(meta_data.t, 4)

        meta_data = wrapper.metadata_from_fname('test_S83_C4_Z5_T6.tif')
        self.assertEqual(meta_data.s, 83)
        
        wrapper.split_order = ['z', 'c']
        meta_data = wrapper.metadata_from_fname('test_Z3_C4.tif')
        self.assertEqual(meta_data.c, 4)
        self.assertEqual(meta_data.z, 3)


    def test_manifest(self):
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        with patch('os.listdir', return_value=[]):
            entry = Mock()
            entry.directory = 'dummy'
            self.assertEqual(wrapper.manifest(entry), [])

        with patch('os.listdir', return_value=['test_S1_C2_Z3_T4.tif']):
            entry = Mock()
            entry.directory = 'dummy'
            fpath = os.path.abspath(os.path.join(entry.directory,
                                                 'test_S1_C2_Z3_T4.tif'))
            self.assertEqual(wrapper.manifest(entry),
                             [{"filename": fpath,
                               "series": 1,
                               "channel": 2,
                               "zslice": 3,
                               "timepoint": 4}])
        
if __name__ == '__main__':
    unittest.main()

