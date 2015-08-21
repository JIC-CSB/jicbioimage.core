import unittest

import numpy as np


class RegionTestCase(unittest.TestCase):

    def test_force_dtype(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])

        region = Region(test_array)
        self.assertEqual(region.dtype, bool)

    def test_region(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])

        region = Region(test_array)

        self.assertFalse(region[0, 0])
        self.assertTrue(region[0, 1])
        self.assertEqual(region.shape, (3, 3))

    def test_region_select_from_array(self):
        from jicbioimage.core.region import Region

        id_array = np.array([[0, 0, 0],
                             [1, 1, 1],
                             [2, 2, 2]])

        region_1 = Region.select_from_array(id_array, 1)

        self.assertFalse(region_1[0, 0])
        self.assertTrue(region_1[1, 0])
        self.assertFalse(region_1[2, 0])

        self.assertEqual(region_1.area, 3)

    def test_region_area(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])

        region = Region(test_array)

        self.assertEqual(region.area, 3)

    def test_region_perimeter(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0]])

        region = Region(test_array)

        self.assertEqual(region.perimeter, 8)

    def test_region_border(self):
        from jicbioimage.core.region import Region

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

        self.assertTrue( np.array_equal(region.border,
            border_region))

    def test_region_inner(self):
        from jicbioimage.core.region import Region

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

        self.assertTrue(np.array_equal(region.inner,
            inner_region))

    def test_force_binary(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 1, 2],
                               [0, 0, 1],
                               [0, 0, 0]])

        binary = np.array(test_array, dtype=bool)

        region = Region(test_array)

        self.assertTrue(np.array_equal(region, binary))

    def test_region_convex_hull(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0],
                               [0, 1, 0, 0, 0],
                               [0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0]])

        region = Region(test_array)

        convex_hull_array = np.array([[0, 0, 0, 0, 0],
                                      [0, 1, 1, 1, 0],
                                      [0, 1, 1, 0, 0],
                                      [0, 1, 0, 0, 0],
                                      [0, 0, 0, 0, 0]], dtype=bool)

        self.assertTrue(np.array_equal(region.convex_hull,
            convex_hull_array))

    def test_index_arrays(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])

        region = Region(test_array)
        x_array, y_array =  region.index_arrays
        self.assertTrue(np.array_equal(x_array, np.array([0, 0, 1])))
        self.assertTrue(np.array_equal(y_array, np.array([1, 2, 2])))

    def test_points(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])

        region = Region(test_array)
        x_array, y_array =  region.index_arrays
        self.assertEqual(region.points,
            [(0,1), (0,2), (1,2)])

    def test_dilate(self):
        from jicbioimage.core.region import Region

        test_array = np.array([[0, 0, 0, 0, 0],
                               [0, 0, 1, 1, 0],
                               [0, 1, 1, 0, 0],
                               [0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0]])

        region = Region(test_array)

        dilate_array = np.array([[0, 0, 1, 1, 0],
                                 [0, 1, 1, 1, 1],
                                 [1, 1, 1, 1, 0],
                                 [1, 1, 1, 0, 0],
                                 [0, 1, 0, 0, 0]], dtype=bool)


        print region.dilate()
        self.assertTrue(np.array_equal(region.dilate(),
            dilate_array))

    def test_repr(self):
        from jicbioimage.core.region import Region
        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])
        region = Region(test_array)
        self.assertEqual(repr(region), repr(region))

    def test_str(self):
        from jicbioimage.core.region import Region
        test_array = np.array([[0, 1, 1],
                               [0, 0, 1],
                               [0, 0, 0]])
        region = Region(test_array)
        self.assertEqual(str(region), str(region))
