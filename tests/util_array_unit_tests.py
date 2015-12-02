"""Tests for the :mod:`jicbioimage.core.util.array` module."""

import unittest
import sys
import numpy as np

class NormaliseTests(unittest.TestCase):

    def test_import_normalise(self):
        # This throws an error if the function cannot be imported.
        from jicbioimage.core.util.array import normalise
        
    def test_normalise_returns_float_array(self):
        from jicbioimage.core.util.array import normalise
        zeros = np.array([1,2,3], dtype=np.uint8)
        normed = normalise(zeros) 
        self.assertEqual(normed.dtype, np.float)
        
    def test_only_zeros(self):
        from jicbioimage.core.util.array import normalise
        zeros = np.zeros(5, dtype=np.float)
        normed = normalise(zeros) 
        self.assertTrue( np.array_equiv(normed, zeros) )

    def test_only_positive(self):
        from jicbioimage.core.util.array import normalise
        ones = np.ones(5, dtype=np.float)
        normed = normalise(ones + 3.) 
        self.assertTrue( np.array_equiv(normed, ones) )

    def test_only_negative(self):
        from jicbioimage.core.util.array import normalise
        zeros = np.zeros(5, dtype=np.float)
        normed = normalise(zeros - 1.) 
        self.assertTrue( np.array_equiv(normed, zeros) )

    def test_normalise_123(self):
        from jicbioimage.core.util.array import normalise
        ar = np.array([1,2,3], dtype=np.uint8)
        normed = normalise(ar)
        expected = np.array([0., .5, 1.], dtype=np.float)
        self.assertTrue( np.array_equiv(normed, expected) )

class ReduceStackTests(unittest.TestCase):

    def test_import_reduce_stack(self):
        # This throws an error if the function cannot be imported.
        from jicbioimage.core.util.array import reduce_stack

    def test_reduce_stack(self):
        from jicbioimage.core.util.array import reduce_stack
        zslice0 = np.array(
            [[0, 1, 2],
             [0, 1, 2],
             [0, 1, 2]], dtype=np.uint8)
        zslice1 = np.array(
            [[2, 1, 0],
             [2, 1, 0],
             [2, 1, 0]], dtype=np.uint8)
        zslice2 = np.array(
            [[0, 0, 0],
             [0, 0, 0],
             [3, 3, 3]], dtype=np.uint8)
        zstack = np.dstack([zslice0, zslice1, zslice2])
        expected = np.array(
            [[2, 1, 2],
             [2, 1, 2],
             [3, 3, 3]], dtype=np.uint8)
        max_projection = reduce_stack(zstack, max)
        self.assertTrue(np.array_equal(expected, max_projection))

class MapStackTests(unittest.TestCase):

    def test_import_map_stack(self):
        # This throws an error if the function cannot be imported.
        from jicbioimage.core.util.array import map_stack

    def test_map_stack(self):
        from jicbioimage.core.util.array import map_stack
        def double(ar):
            return ar * 2
        zslice0 = np.array(
            [[0, 1, 2],
             [0, 1, 2],
             [0, 1, 2]], dtype=np.uint8)
        zslice1 = np.array(
            [[2, 1, 0],
             [2, 1, 0],
             [2, 1, 0]], dtype=np.uint8)
        zstack = np.dstack([zslice0, zslice1])
        expected = np.dstack([double(zslice0), double(zslice1)])

        mapped = map_stack(zstack, double)
        self.assertTrue(np.array_equal(expected, mapped))

class CheckDTypeTests(unittest.TestCase):

    def test_import_check_dtype(self):
        # This throws an error if the function cannot be imported.
        from jicbioimage.core.util.array import check_dtype

    def test_disallowed_raises_TypeError(self):
        from jicbioimage.core.util.array import check_dtype
        ar = np.zeros((5,5), dtype=np.uint64)
        with self.assertRaises(TypeError):
            check_dtype(ar, np.uint8)

    def test_allowed_does_not_raise_TypeError(self):
        from jicbioimage.core.util.array import check_dtype
        ar = np.zeros((5,5), dtype=np.uint64)
        check_dtype(ar, np.uint64)

    def test_check_dtype_with_allowed_as_list(self):
        from jicbioimage.core.util.array import check_dtype
        ar = np.zeros((5,5), dtype=np.uint64)
        check_dtype(ar, [np.uint8, np.uint16, np.uint64])

class DTypeContract(unittest.TestCase):
    
    def test_import_dtype_contract(self):
        # This throws an error if the function cannot be imported.
        from jicbioimage.core.util.array import dtype_contract
        
    def test_input_dtype_only(self):
        from jicbioimage.core.util.array import dtype_contract
        @dtype_contract(input_dtype=np.uint8)
        def some_func(ar):
            return ar

        # This should not raise any error. 
        ar = some_func( np.zeros((2,2), dtype=np.uint8) )
        
        # However, this should.
        with self.assertRaises(TypeError):
            ar = some_func( np.zeros((2,2), dtype=np.uint64) )
        
    def test_output_dtype_only(self):
        from jicbioimage.core.util.array import dtype_contract
        @dtype_contract(output_dtype=np.uint8)
        def some_func(ar):
            return ar

        # This should not raise any error. 
        ar = some_func( np.zeros((2,2), dtype=np.uint8) )
        
        # However, this should.
        with self.assertRaises(TypeError):
            ar = some_func( np.zeros((2,2), dtype=np.uint64) )
        
    def test_input_and_output_dtypes(self):
        from jicbioimage.core.util.array import dtype_contract
        @dtype_contract(input_dtype=np.uint8, output_dtype=np.uint64)
        def working_func(ar):
            return ar.astype(np.uint64)

        # This should not raise any error. 
        ar = working_func( np.zeros((2,2), dtype=np.uint8) )
        # However, this should (wrong input).
        with self.assertRaises(TypeError):
            ar = working_func( np.zeros((2,2), dtype=np.uint64) )

        # Function generates wrong output dtype.
        @dtype_contract(input_dtype=np.uint8, output_dtype=np.uint8)
        def broken_func(ar):
            return ar.astype(np.uint64)

        with self.assertRaises(TypeError):
            ar = broken_func( np.zeros((2,2), dtype=np.uint8) )

    def test_function_name_not_mangled(self):
        from jicbioimage.core.util.array import dtype_contract
        @dtype_contract(input_dtype=np.uint8, output_dtype=np.uint64)
        def working_func(ar):
            return ar.astype(np.uint64)
        
        self.assertEqual(working_func.__name__, "working_func")

class FalseColorTests(unittest.TestCase):


    def test_import_false_color(self):

        from jicbioimage.core.util.array import false_color

    def test_false_color_dimensions(self):

        from jicbioimage.core.util.array import false_color

        input_array = np.zeros((10,))
        self.assertEqual(false_color(input_array).shape, (10, 3))

        input_array = np.zeros((10, 20))
        self.assertEqual(false_color(input_array).shape, (10, 20, 3))

        input_array = np.zeros((10, 20, 30))
        self.assertEqual(false_color(input_array).shape, (10, 20, 30, 3))

    def test_false_color_dtype(self):

        from jicbioimage.core.util.array import false_color

        input_array = np.zeros((10, 20))
        self.assertEqual(false_color(input_array).dtype, np.uint8)

    def test_false_color_with_custom_palette(self):

        from jicbioimage.core.util.array import false_color

        input_array = np.array([[0, 0, 0],
                                [1, 1, 1],
                                [2, 2, 2]])

        c1 = [255, 0, 0]
        c2 = [0, 255, 0]
        c3 = [0, 0, 255]

        color_dict = {0 : c1, 1 : c2, 2 : c3}

        expected_output = np.array([[c1, c1, c1],
                                    [c2, c2, c2],
                                    [c3, c3, c3]], dtype=np.uint8)
                                   
        actual_output = false_color(input_array, color_dict)

        self.assertTrue(np.array_equal(actual_output, expected_output))

    def test_false_color_with_default_palette_with_background_colored(self):

        from jicbioimage.core.util.array import false_color

        input_array = np.array([[0, 0, 0],
                                [1, 1, 1],
                                [2, 2, 2]])

        c1 = [228, 90, 135]
        c2 = [132, 27, 117]
        c3 = [20, 134, 44]

        expected_output = np.array([[c1, c1, c1],
                                    [c2, c2, c2],
                                    [c3, c3, c3]], dtype=np.uint8)
                                   
        actual_output = false_color(input_array, keep_zero_black=False)

        self.assertTrue(np.array_equal(actual_output, expected_output))

    def test_false_color_with_default_palette(self):

        from jicbioimage.core.util.array import false_color

        input_array = np.array([[0, 0, 0],
                                [1, 1, 1],
                                [2, 2, 2]])

        c1 = [0, 0, 0]
        c2 = [132, 27, 117]
        c3 = [20, 134, 44]

        expected_output = np.array([[c1, c1, c1],
                                    [c2, c2, c2],
                                    [c3, c3, c3]], dtype=np.uint8)
                                   
        actual_output = false_color(input_array)

        self.assertTrue(np.array_equal(actual_output, expected_output))



if __name__ == '__main__':
    unittest.main()