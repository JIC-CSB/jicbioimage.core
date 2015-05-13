"""Unit tests for the Point2D class."""

import unittest

class Point2DUnitTests(unittest.TestCase):
    
    def test_import(self):
        # This throws an error if the class cannot be imported.
        from jicimagelib.geometry import Point2D

    def test_initialisation_with_tuple(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( (1, 2) )
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        
    def test_initialisation_with_x_y_values(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( 1, 2 )
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        
        

if __name__ == '__main__':
    unittest.main()
