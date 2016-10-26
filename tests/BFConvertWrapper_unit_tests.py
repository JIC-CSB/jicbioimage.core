"""Tests for the :class:`jicbioimage.core.image.BFConvertWrapper` class."""

import sys
import unittest
import os.path

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

HERE = os.path.dirname(__file__)

class BFConvertWrapperTests(unittest.TestCase):

    def setUp(self):
        self.org_sys_platform = sys.platform

    def tearDown(self):
        sys.platform = self.org_sys_platform

    def test_backend_attribute(self):
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        self.assertEqual(wrapper.backend, 'backend')

    def test_split_order(self):
        """Test the split_order attribute."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        self.assertEqual(wrapper._split_order, ['s', 'c', 'z', 't'])

    def test_split_pattern(self):
        """Test the split_pattern property."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        self.assertEqual(wrapper.split_pattern(), 'S%s_C%c_Z%z_T%t')
        self.assertEqual(wrapper.split_pattern(win32=True), 'S%%s_C%%c_Z%%z_T%%t')

    def test_run_command_linux(self):
        """Test the run_command function."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')

        sys.platform = 'linux2'

        cmd = wrapper.run_command('test.lif')
        self.assertEqual(cmd, ['bfconvert',
                               '-nolookup',
                               'test.lif',
                               'S%s_C%c_Z%z_T%t.tif'])

        cmd = wrapper.run_command('test.lif', output_dir=os.path.join('/', 'tmp'))
        self.assertEqual(cmd, ['bfconvert',
                               '-nolookup',
                               'test.lif',
                               os.path.join('/', 'tmp', 'S%s_C%c_Z%z_T%t.tif')])

    def test_run_command_windows(self):
        """Test the run_command function."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')

        sys.platform = 'win32'

        cmd = wrapper.run_command('test.lif')
        self.assertEqual(cmd, ['bfconvert.bat',
                               '-nolookup',
                               'test.lif',
                               'S%%s_C%%c_Z%%z_T%%t.tif'])

        cmd = wrapper.run_command('test.lif', output_dir=os.path.join('/', 'tmp'))
        self.assertEqual(cmd, ['bfconvert.bat',
                               '-nolookup',
                               'test.lif',
                               os.path.join('/', 'tmp', 'S%%s_C%%c_Z%%z_T%%t.tif')])

    def test_metadata_from_fname(self):
        """Test the metadata_from_fname function."""
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')

        meta_data = wrapper.metadata_from_fname("S1_C2_Z3_T4.tif", md5_hexdigest="dummy")
        self.assertEqual(meta_data["filename"], "S1_C2_Z3_T4.tif")
        self.assertEqual(meta_data["md5_hexdigest"], "dummy")
        self.assertEqual(meta_data["series"], 1)
        self.assertEqual(meta_data["channel"], 2)
        self.assertEqual(meta_data["zslice"], 3)
        self.assertEqual(meta_data["timepoint"], 4)

        meta_data = wrapper.metadata_from_fname('S83_C4_Z5_T6.tif', md5_hexdigest="dummy")
        self.assertEqual(meta_data["series"], 83)

    def test_manifest(self):
        from jicbioimage.core.io import BFConvertWrapper
        wrapper = BFConvertWrapper('backend')
        with patch('os.listdir', return_value=[]):
            entry = Mock()
            entry.directory = 'dummy'
            self.assertEqual(wrapper.manifest(entry), [])

        with patch('os.listdir', return_value=['S1_C2_Z3_T4.tif']),  \
             patch('jicbioimage.core.io._md5_hexdigest_from_file', return_value="dummy_hexdigest"):
            entry = Mock()
            entry.directory = 'dummy'
            self.assertEqual(wrapper.manifest(entry),
                             [{"filename": 'S1_C2_Z3_T4.tif',
                               "md5_hexdigest": "dummy_hexdigest",
                               "series": 1,
                               "channel": 2,
                               "zslice": 3,
                               "timepoint": 4}])

if __name__ == '__main__':
    unittest.main()

