"""Do some basic tests."""

import unittest

class TestBasics(unittest.TestCase):
    """Test the basics of the jicimage package."""

    def test_import(self):
        """Test importing the package."""
        # This throws an error if the module cannot be imported.
        import jicimagelib

    def test_version(self):
        """Test that there is a version numer."""
        import jicimagelib
        self.assertTrue(isinstance(jicimagelib.__version__, float))
