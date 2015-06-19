"""Do some basic tests."""

import unittest

class TransformationDecoratorTests(unittest.TestCase):

    def test_is_callable(self):
        from jicimagelib.transform import transformation
        self.assertTrue(callable(transformation))

    def test_returns_callable(self):
        from jicimagelib.transform import transformation
        def tmp():
            pass
        decorated = transformation(tmp)
        self.assertTrue(callable(decorated))

    def test_uint64_image_raises_when_auto_safe_dtype_is_false(self):
        from jicimagelib.transform import transformation
        from jicimagelib.io import AutoWrite
        import numpy as np
        AutoWrite.auto_safe_dtype = False
        def some_transform(image):
            return image
        decorated = transformation(some_transform)
        im = np.zeros((50,50), dtype=np.uint64)
        with self.assertRaisesRegexp(TypeError,
            "Cannot handle this data type: uint64"):
            decorated(im)

class TransformTests(unittest.TestCase):

    def test_import_max_intensity_projection(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.transform import max_intensity_projection
    
    def test_import_min_intensity_projection(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.transform import min_intensity_projection
    
    def test_import_smooth_gaussian(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.transform import smooth_gaussian

    def test_equalize_adaptive_clahe(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.transform import equalize_adaptive_clahe

    def test_import_remove_small_objects(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.transform import remove_small_objects

    def test_threshold_otsu(self):
        # This throws an error if the function cannot be imported.
        from jicimagelib.transform import threshold_otsu

if __name__ == '__main__':
    unittest.main()
