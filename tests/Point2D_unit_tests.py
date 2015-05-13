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
        self.assertEqual(repr(p), "<Point2D(x=1, y=2, dtype=int)>")
        
    def test_repr_float(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( 1.33333333333333 , 2.66666666667 )
        self.assertEqual(repr(p), "<Point2D(x=1.33, y=2.67, dtype=float)>")
        
    def test_dtype_int(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( 1 , 2 )
        self.assertEqual(p.dtype, "int")
        self.assertTrue(isinstance(p.x, int))
        self.assertTrue(isinstance(p.y, int))

    def test_dtype_float(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( 1.0 , 2.0 )
        self.assertEqual(p.dtype, "float")
        self.assertTrue(isinstance(p.x, float))
        self.assertTrue(isinstance(p.y, float))

    def test_dtype_mixed(self):
        from jicimagelib.geometry import Point2D
        p = Point2D( 1 , 2.0 )
        self.assertEqual(p.dtype, "float")
        self.assertTrue(isinstance(p.x, float))
        self.assertTrue(isinstance(p.y, float))

    def test_assert_non_numeric_raises_runtime_error(self):
        from jicimagelib.geometry import Point2D
        with self.assertRaises(RuntimeError):
            p = Point2D( "1" , 2.0 )
        
    def test_equal(self):
        from jicimagelib.geometry import Point2D
        p1 = Point2D(1, 1)
        p2 = Point2D(1, 1)
        self.assertTrue(p1 == p2) 

    def test_Point2D_of_different_dtypes_not_equal(self):
        from jicimagelib.geometry import Point2D
        p1 = Point2D(1, 1)
        p2 = Point2D(1.0, 1.0)
        self.assertFalse(p1 == p2) 

    def test_add(self):
        from jicimagelib.geometry import Point2D
        p = Point2D(2,3)
        self.assertEqual(p+p, Point2D(4,6))

    def test_add_int_float_mixed(self):
        from jicimagelib.geometry import Point2D
        p1 = Point2D(2,3)
        p2 = Point2D(2.0,3.0)
        self.assertEqual(p1+p2, Point2D(4.0,6.0))
        
    def test_sub(self):
        from jicimagelib.geometry import Point2D
        p1 = Point2D(2,3)
        p2 = Point2D(3, 1)
        self.assertEqual(p1-p2, Point2D(-1,2))
        
    def test_sub_int_float_mixed(self):
        from jicimagelib.geometry import Point2D
        p1 = Point2D(2,3)
        p2 = Point2D(3.0, 1.0)
        self.assertEqual(p1-p2, Point2D(-1.0,2.0))
        
    def test_mul_with_Point2D(self):
        from jicimagelib.geometry import Point2D
        p = Point2D(2,3)
        self.assertEqual(p*p, Point2D(4,9))
        
    def test_mul_with_int(self):
        from jicimagelib.geometry import Point2D
        p = Point2D(2,3)
        self.assertEqual(p*3, Point2D(6,9))
        
    def test_mul_with_float(self):
        from jicimagelib.geometry import Point2D
        p = Point2D(2,3)
        self.assertEqual(p*3.0, Point2D(6.0,9.0))
        
if __name__ == '__main__':
    unittest.main()
