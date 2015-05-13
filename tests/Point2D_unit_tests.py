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
        
    def test_repr_int(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( 1, 2 )
        self.assertEqual(repr(p), "<Point2D(x=1, y=2)>")
        
    def test_repr_float(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( 1.33333333333333 , 2.66666666667 )
        self.assertEqual(repr(p), "<Point2D(x=1.33, y=2.67)>")
        
        

if __name__ == '__main__':
    unittest.main()
