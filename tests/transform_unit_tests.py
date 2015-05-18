"""Do some basic tests."""

import unittest

class TestTransformationDecorator(unittest.TestCase):

    def test_is_callable(self):
        from jicimagelib.transform import transformation
        self.assertTrue(callable(transformation))

    def test_returns_callable(self):
        from jicimagelib.transform import transformation
        def tmp():
            pass
        decorated = transformation(tmp)
        self.assertTrue(callable(decorated))

    def test_uint64_image_raises(self):
        from jicimagelib.transform import transformation
        import numpy as np
        def some_tranform(image):
            return image
        decorated = transformation(some_tranform)
        im = np.zeros((50,50), dtype=np.uint64)
        with self.assertRaisesRegexp(TypeError,
            "Cannot handle this data type: uint64"):
            decorated(im)

if __name__ == '__main__':
    unittest.main()
