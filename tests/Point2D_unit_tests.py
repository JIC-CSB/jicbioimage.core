"""Unit tests for the Point2D class."""

import unittest

class Point2DUnitTests(unittest.TestCase):
    
    def test_import(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.geometry import Point2D
        

if __name__ == '__main__':
    unittest.main()
