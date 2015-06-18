"""Tests for the :mod:`jicimagelib.util.array` module."""

import unittest
import numpy as np

class NormaliseTests(unittest.TestCase):

    def test_import_normalise(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.util.array import normalise
        
    def test_normalise_returns_float_array(self):
        from jicimagelib.util.array import normalise
        zeros = np.array([1,2,3], dtype=np.uint8)
        normed = normalise(zeros) 
        self.assertEqual(normed.dtype, np.float)
        
    def test_only_zeros(self):
        from jicimagelib.util.array import normalise
        zeros = np.zeros(5, dtype=np.float)
        normed = normalise(zeros) 
        self.assertTrue( np.array_equiv(normed, zeros) )

    def test_only_positive(self):
        from jicimagelib.util.array import normalise
        ones = np.ones(5, dtype=np.float)
        normed = normalise(ones + 3.) 
        self.assertTrue( np.array_equiv(normed, ones) )

    def test_only_negative(self):
        from jicimagelib.util.array import normalise
        zeros = np.zeros(5, dtype=np.float)
        normed = normalise(zeros - 1.) 
        self.assertTrue( np.array_equiv(normed, zeros) )

    def test_normalise_123(self):
        from jicimagelib.util.array import normalise
        ar = np.array([1,2,3], dtype=np.uint8)
        normed = normalise(ar)
        expected = np.array([0., .5, 1.], dtype=np.float)
        self.assertTrue( np.array_equiv(normed, expected) )

class ProjectByFunctionTests(unittest.TestCase):

    def test_import_project_by_function(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.util.array import project_by_function

    def test_project_by_function(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.util.array import project_by_function
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
        max_projection = project_by_function(zstack, max)
        self.assertTrue(np.array_equal(expected, max_projection))

class CheckDTypeTests(unittest.TestCase):

    def test_import_check_dtype(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.util.array import check_dtype

    def test_disallowed_raises_TypeError(self):
        from jicimagelib.util.array import check_dtype
        ar = np.zeros((5,5), dtype=np.uint64)
        with self.assertRaises(TypeError):
            check_dtype(ar, np.uint8)

    def test_allowed_does_not_raise_TypeError(self):
        from jicimagelib.util.array import check_dtype
        ar = np.zeros((5,5), dtype=np.uint64)
        check_dtype(ar, np.uint64)

    def test_check_dtype_with_allowed_as_list(self):
        from jicimagelib.util.array import check_dtype
        ar = np.zeros((5,5), dtype=np.uint64)
        check_dtype(ar, [np.uint8, np.uint16, np.uint64])

class DTypeContract(unittest.TestCase):
    
    def test_import_dtype_contract(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.util.array import dtype_contract
        
    def test_input_dtype_only(self):
        from jicimagelib.util.array import dtype_contract
        @dtype_contract(input_dtype=np.uint8)
        def some_func(ar):
            return ar

        # This should not raise any error. 
        ar = some_func( np.zeros((2,2), dtype=np.uint8) )
        
        # However, this should.
        with self.assertRaises(TypeError):
            ar = some_func( np.zeros((2,2), dtype=np.uint64) )
        
    def test_output_dtype_only(self):
        from jicimagelib.util.array import dtype_contract
        @dtype_contract(output_dtype=np.uint8)
        def some_func(ar):
            return ar

        # This should not raise any error. 
        ar = some_func( np.zeros((2,2), dtype=np.uint8) )
        
        # However, this should.
        with self.assertRaises(TypeError):
            ar = some_func( np.zeros((2,2), dtype=np.uint64) )
        
    def test_input_and_output_dtypes(self):
        from jicimagelib.util.array import dtype_contract
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
