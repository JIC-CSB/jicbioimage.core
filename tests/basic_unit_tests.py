"""Do some basic tests."""

import unittest

class TestBasics(unittest.TestCase):
    """Test the basics of the jicimage package."""

    def test_import_package(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib

    def test_version(self):
        import jicimagelib
        self.assertTrue(isinstance(jicimagelib.__version__, str))

    def test_import_image_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.image

    def test_import_io_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.io

    def test_import_geometry_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.geometry

    def test_import_transform_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.transform

    def test_import_region_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.region

    def test_import_DataManager_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import DataManager

    def test_import_ImageCollection_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import ImageCollection

    def test_import_ProxyImage_class(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.image import ProxyImage

    def test_import_util_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.util

    def test_import_util_array_module(self):
        # This throws an error if the module cannot be imported.
        import jicimagelib.util.array

if __name__ == '__main__':
    unittest.main()
