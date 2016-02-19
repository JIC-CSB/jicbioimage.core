"""Do some basic tests."""

import unittest

class TestBasics(unittest.TestCase):
    """Test the basics of the jicimage package."""

    def test_import_package(self):
        # This throws an error if the module cannot be imported.
        import jicbioimage.core

    def test_version(self):
        import jicbioimage.core
        self.assertTrue(isinstance(jicbioimage.core.__version__, str))

    def test_import_image_module(self):
        # This throws an error if the module cannot be imported.
        import jicbioimage.core.image

    def test_import_io_module(self):
        # This throws an error if the module cannot be imported.
        import jicbioimage.core.io

    def test_import_transform_module(self):
        # This throws an error if the module cannot be imported.
        import jicbioimage.core.transform

    def test_import_DataManager_class(self):
        # This throws an error if the class cannot be imported.
        from jicbioimage.core.image import DataManager

    def test_import_ImageCollection_class(self):
        # This throws an error if the class cannot be imported.
        from jicbioimage.core.image import ImageCollection

    def test_import_ProxyImage_class(self):
        # This throws an error if the class cannot be imported.
        from jicbioimage.core.image import ProxyImage

    def test_import_util_module(self):
        # This throws an error if the module cannot be imported.
        import jicbioimage.core.util

    def test_import_util_array_module(self):
        # This throws an error if the module cannot be imported.
        import jicbioimage.core.util.array

if __name__ == '__main__':
    unittest.main()
