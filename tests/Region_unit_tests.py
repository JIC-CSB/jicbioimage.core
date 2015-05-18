import unittest

import numpy as np


class RegionTestCase(unittest.TestCase):

    def test_region(self):
        from jicimagelib.region import Region

        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])

        region = Region(test_array)

        bitmap = region.bitmap

        self.assertFalse(bitmap[0, 0])
        self.assertTrue(bitmap[0, 1])
        self.assertEqual(bitmap.shape, (3, 3))

    def test_region_from_id_array(self):
        from jicimagelib.region import Region

        id_array = np.array([[0, 0, 0],
                             [1, 1, 1],
                             [2, 2, 2]])

        region_1 = Region.from_id_array(id_array, 1)

        self.assertFalse(region_1.bitmap[0, 0])
        self.assertTrue(region_1.bitmap[1, 0])
        self.assertFalse(region_1.bitmap[2, 0])

        self.assertEqual(region_1.area, 3)

    def test_region_area(self):
        from jicimagelib.region import Region

        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])

        region = Region(test_array)

        self.assertEqual(region.area, 3)

    def test_region_perimeter(self):
        from jicimagelib.region import Region

        test_array = np.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0]])

        region = Region(test_array)

        self.assertEqual(region.perimeter, 8)

    def test_region_border(self):
        from jicimagelib.region import Region

        test_array = np.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0]])

        region = Region(test_array)

        border_array = np.array([[0, 0, 0, 0, 0],
                                 [0, 1, 1, 1, 0],
                                 [0, 1, 0, 1, 0],
                                 [0, 1, 1, 1, 0],
                                 [0, 0, 0, 0, 0]])

        border_region = Region(border_array)

        self.assertTrue( np.array_equal(region.border.bitmap,
            border_region.bitmap))

    def test_region_inner(self):
        from jicimagelib.region import Region

        test_array = np.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0]])

        region = Region(test_array)

        inner_array = np.array([[0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0]])

        inner_region = Region(inner_array)

        self.assertTrue(np.array_equal(region.inner.bitmap,
            inner_region.bitmap))

    def test_region_constructor(self):
        from jicimagelib.region import Region

        test_array = np.array([[0, 1, 2],
                               [0, 0, 1],
                               [0, 0, 0]])

        with self.assertRaises(ValueError):
            Region(test_array)
