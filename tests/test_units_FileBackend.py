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
        from jicimagelib.image import FileBackend
        backend = FileBackend()
        self.assertEqual(backend.base_dir, CURRENT_WORKING_DIR)

    def test_instantiation_with_base_dir_specified(self):
        from jicimagelib.image import FileBackend
        base_dir = os.path.join(TMP_DIR, 'jicimagelib')
        self.assertFalse(os.path.isdir(base_dir))
        backend = FileBackend(base_dir=base_dir)
        self.assertEqual(backend.base_dir, base_dir)
        self.assertTrue(os.path.isdir(base_dir))
        
    def test_modifying_base_dir_post_instantiation(self):
        from jicimagelib.image import FileBackend
        backend = FileBackend()
        base_dir = os.path.join(TMP_DIR, 'jicimagelib')
        self.assertFalse(os.path.isdir(base_dir))
        backend.base_dir = base_dir
        self.assertTrue(os.path.isdir(base_dir))

    def test_new_entry(self):
        from jicimagelib.image import FileBackend
        base_dir = os.path.join(TMP_DIR, 'jicimagelib')
        backend = FileBackend(base_dir=base_dir)
        entry = backend.new_entry('test.lif')
        self.assertTrue(isinstance(entry, FileBackend.Entry))
        parent_dir, entry_dir = os.path.split(entry.directory)
        self.assertEqual(parent_dir, base_dir)
        self.assertEqual(entry_dir, 'test.lif')
        
    def test_new_entry_gives_unique_base_dirs(self):
        from jicimagelib.image import FileBackend
        base_dir = os.path.join(TMP_DIR, 'jicimagelib')
        backend = FileBackend(base_dir=base_dir)
        entry1 = backend.new_entry('file1.lif')
        entry2 = backend.new_entry('file2.lif')
        parent_dir, entry_dir1 = os.path.split(entry1.directory)
        parent_dir, entry_dir2 = os.path.split(entry2.directory)
        self.assertNotEqual(entry_dir1, entry_dir2)
        
    def test_entry_directory_exists(self):
        from jicimagelib.image import FileBackend
        base_dir = os.path.join(TMP_DIR, 'jicimagelib')
        backend = FileBackend(base_dir=base_dir)
        entry = backend.new_entry('test.lif')
        self.assertTrue(os.path.isdir(entry.directory))
        
if __name__ == '__main__':
    unittest.main()
