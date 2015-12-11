"""Tests for the :class:`jicbioimage.core.io.AutoName` class."""

import unittest
import os.path


class AutoNameTests(unittest.TestCase):

    def tearDown(self):
        from jicbioimage.core.io import AutoName
        AutoName.count = 0
        AutoName.prefix_format = "{:d}_"
        AutoName.suffix = ".png"

    def test_count(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.count, 0)

    def test_directory(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.directory, None)

    def test_suffix(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.suffix, '.png')

    def test_prefix_format_default(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.prefix_format, "{:d}_")

    def test_prefix(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.prefix(), "0_")

    def test_custom_prefix(self):
        from jicbioimage.core.io import AutoName
        AutoName.prefix_format = "{:02d}_"
        self.assertEqual(AutoName.prefix(), "00_")

    def test_name_callable(self):
        from jicbioimage.core.io import AutoName
        self.assertTrue(callable(AutoName.name))

    def test_name_logic(self):
        from jicbioimage.core.io import AutoName

        def no_transform(image):
            return image

        self.assertEqual(AutoName.name(no_transform), '1_no_transform.png')
        AutoName.directory = os.path.join('/', 'tmp')
        self.assertEqual(AutoName.name(no_transform),
                         os.path.join('/', 'tmp', '2_no_transform.png'))

    def test_custom_suffix_name_logic(self):
        from jicbioimage.core.io import AutoName
        AutoName.suffix = ".tiff"

        def no_transform(image):
            return image

        self.assertEqual(AutoName.name(no_transform), '1_no_transform.tiff')

    def test_custom_prefix_name_logic(self):
        from jicbioimage.core.io import AutoName
        AutoName.prefix_format = "{:02d}_"

        def no_transform(image):
            return image

        self.assertEqual(AutoName.name(no_transform), '01_no_transform.png')

if __name__ == '__main__':
    unittest.main()
