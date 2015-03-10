"""Tests for the :class:`jicimagelib.image.FileBackend` class."""

import unittest
import os
import os.path
import shutil

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
        from jicimagelib.io import FileBackend
        directory = os.path.join(TMP_DIR, 'jicimagelib')
        self.assertFalse(os.path.isdir(directory))
        backend = FileBackend(directory=directory)
        self.assertEqual(backend.directory, directory)
        self.assertTrue(os.path.isdir(directory))
        
    def test_modifying_directory_post_instantiation_raises(self):
        from jicimagelib.io import FileBackend
        directory = os.path.join(TMP_DIR, 'jicimagelib')
        backend = FileBackend(directory)
        with self.assertRaises(AttributeError):
            backend.directory = 'dummy'

    def test_new_entry(self):
        from jicimagelib.io import FileBackend
        directory = os.path.join(TMP_DIR, 'jicimagelib')
        backend = FileBackend(directory=directory)
        entry = backend.new_entry('test.lif')
        self.assertTrue(isinstance(entry, FileBackend.Entry))
        parent_dir, entry_dir = os.path.split(entry.directory)
        self.assertEqual(parent_dir, directory)
        self.assertEqual(entry_dir, 'test.lif')
        
    def test_new_entry_gives_unique_directories(self):
        from jicimagelib.io import FileBackend
        directory = os.path.join(TMP_DIR, 'jicimagelib')
        backend = FileBackend(directory=directory)
        entry1 = backend.new_entry('file1.lif')
        entry2 = backend.new_entry('file2.lif')
        parent_dir, entry_dir1 = os.path.split(entry1.directory)
        parent_dir, entry_dir2 = os.path.split(entry2.directory)
        self.assertNotEqual(entry_dir1, entry_dir2)
        
    def test_entry_directory_exists(self):
        from jicimagelib.io import FileBackend
        directory = os.path.join(TMP_DIR, 'jicimagelib')
        backend = FileBackend(directory=directory)
        entry = backend.new_entry('test.lif')
        self.assertTrue(os.path.isdir(entry.directory))
        
if __name__ == '__main__':
    unittest.main()
