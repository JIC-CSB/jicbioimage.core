"""Tests for the :class:`jicimagelib.io.AutoName` class."""

import unittest

class AutoNameTests(unittest.TestCase):

    def test_import_AutoName_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.io import AutoName

    def test_count(self):
        from jicimagelib.io import AutoName
        self.assertEqual(AutoName.count, 0)
        
    def test_directory(self):
        from jicimagelib.io import AutoName
        self.assertEqual(AutoName.directory, None)
        
    def test_suffix(self):
        from jicimagelib.io import AutoName
        self.assertEqual(AutoName.suffix, '.png')

    def test_name_callable(self):
        from jicimagelib.io import AutoName
        self.assertTrue(callable(AutoName.name))
        
    def test_name_logic(self): 
        from jicimagelib.io import AutoName
        def no_transform(image):
            return image
        self.assertEqual(AutoName.name(no_transform), '1_no_transform.png')

if __name__ == '__main__':
    unittest.main()
