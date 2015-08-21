"""Do some basic tests."""

import unittest

class TransformationDecoratorTests(unittest.TestCase):

    def test_is_callable(self):
        from jicbioimage.core.transform import transformation
        self.assertTrue(callable(transformation))

    def test_returns_callable(self):
        from jicbioimage.core.transform import transformation
        def tmp():
            pass
        decorated = transformation(tmp)
        self.assertTrue(callable(decorated))

    def test_uint64_image_raises_when_auto_safe_dtype_is_false(self):
        from jicbioimage.core.transform import transformation
        from jicbioimage.core.io import AutoWrite
        import numpy as np
        AutoWrite.auto_safe_dtype = False
        def some_transform(image):
            return image
        decorated = transformation(some_transform)
        im = np.zeros((50,50), dtype=np.uint64)
        with self.assertRaisesRegexp(TypeError,
            "Cannot handle this data type: uint64"):
            decorated(im)

if __name__ == '__main__':
    unittest.main()
