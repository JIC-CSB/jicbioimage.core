"""Tests for the :mod:`jicimagelib.util.array` module."""

import unittest
import numpy as np

class UtilArrayTests(unittest.TestCase):

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

    def test_only_positive(self):
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
