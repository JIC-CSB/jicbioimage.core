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

if __name__ == '__main__':
    unittest.main()
