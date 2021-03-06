"""Unit tests for TemporaryFilePath class."""

import unittest
import os.path

class TemporaryFilePathTests(unittest.TestCase):
    
    def test_suffix(self):
        from jicbioimage.core.image import _TemporaryFilePath
        with _TemporaryFilePath(suffix='.png') as tmp:
            self.assertTrue(tmp.fpath.endswith('.png'))

    def test_fpath_creation(self):
        from jicbioimage.core.image import _TemporaryFilePath
        with _TemporaryFilePath(suffix='.png') as tmp:
            self.assertTrue(os.path.isfile(tmp.fpath))

    def test_fpath_cleanup(self):
        from jicbioimage.core.image import _TemporaryFilePath
        with _TemporaryFilePath(suffix='.png') as tmp:
            pass
        self.assertFalse(os.path.isfile(tmp.fpath))

if __name__ == "__main__":
    unittest.main()
