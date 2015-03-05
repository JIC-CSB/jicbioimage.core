"""Do some basic tests."""

import unittest

class TestBasics(unittest.TestCase):
    """Test the basics of the jicimage package."""

    def test_import_package(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib

    def test_version(self):
        import jicimagelib
        self.assertTrue(isinstance(jicimagelib.__version__, float))

    def test_import_image_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.image

    def test_import_DataManager_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import DataManager

    def test_import_ImageCollection_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import ImageCollection

    def test_import_ImageProxy_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import ImageProxy

    def test_import_ImageProxy_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import ImageProxy


if __name__ == '__main__':
    unittest.main()
