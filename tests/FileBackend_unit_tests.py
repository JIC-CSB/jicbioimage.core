"""Tests for the :class:`jicbioimage.core.image.FileBackend` class."""

import unittest
import os
import os.path
import shutil

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

import jicbioimage.core.io

CURRENT_WORKING_DIR = os.getcwd()
HERE = os.path.dirname(__file__)
TMP_DIR = os.path.join(HERE, 'tmp')

class FileBackendTests(unittest.TestCase):
    
    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        if os.path.isdir(TMP_DIR):
            shutil.rmtree(TMP_DIR)

    def test_default_instantiaiton(self):
        from jicbioimage.core.io import FileBackend
        directory = os.path.join(TMP_DIR, 'jicbioimage.core')
        self.assertFalse(os.path.isdir(directory))
        backend = FileBackend(directory=directory)
        self.assertEqual(backend.directory, directory)
        self.assertTrue(os.path.isdir(directory))
        
    def test_modifying_directory_post_instantiation_raises(self):
        from jicbioimage.core.io import FileBackend
        directory = os.path.join(TMP_DIR, 'jicbioimage.core')
        backend = FileBackend(directory)
        with self.assertRaises(AttributeError):
            backend.directory = 'dummy'

    @patch("jicbioimage.core.io._md5_hexdigest_from_file")
    def test_new_entry(self, patch):
        from jicbioimage.core.io import FileBackend
        import jicbioimage.core.io
        patch.return_value = "1234"
        directory = os.path.join(TMP_DIR, 'jicbioimage.core')
        backend = FileBackend(directory=directory)
        entry = backend.new_entry('test.lif')
        self.assertTrue(isinstance(entry, FileBackend.Entry))
        parent_dir, entry_dir = os.path.split(entry.directory)
        self.assertEqual(parent_dir, directory)
        self.assertEqual(entry_dir, '1234')
        
    @patch("jicbioimage.core.io._md5_hexdigest_from_file")
    def test_new_entry_gives_unique_directories(self, patch):
        from jicbioimage.core.io import FileBackend
        import jicbioimage.core.io
        directory = os.path.join(TMP_DIR, 'jicbioimage.core')
        backend = FileBackend(directory=directory)
        patch.return_value = "1234"
        entry1 = backend.new_entry('file1.lif')
        patch.return_value = "5678"
        entry2 = backend.new_entry('file2.lif')
        parent_dir, entry_dir1 = os.path.split(entry1.directory)
        parent_dir, entry_dir2 = os.path.split(entry2.directory)
        self.assertNotEqual(entry_dir1, entry_dir2)
        
    @patch("jicbioimage.core.io._md5_hexdigest_from_file")
    def test_entry_directory_exists(self, patch):
        from jicbioimage.core.io import FileBackend
        import jicbioimage.core.io
        patch.return_value = "1234"
        directory = os.path.join(TMP_DIR, 'jicbioimage.core')
        backend = FileBackend(directory=directory)
        entry = backend.new_entry('test.lif')
        self.assertTrue(os.path.isdir(entry.directory))
        
if __name__ == '__main__':
    unittest.main()
