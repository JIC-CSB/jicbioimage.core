"""Tests for the :class:`jicimagelib.io.AutoWrite` class."""

import unittest

class AutoWriteTests(unittest.TestCase):

    def test_import_AutoWrite_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.io import AutoWrite

    def test_on(self):
        from jicimagelib.io import AutoWrite
        self.assertTrue(AutoWrite.on)

    def test_auto_safe_dtype(self):
        from jicimagelib.io import AutoWrite
        self.assertTrue(AutoWrite.auto_safe_dtype)
        
        
if __name__ == '__main__':
    unittest.main()
