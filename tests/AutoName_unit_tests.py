"""Tests for the :class:`jicbioimage.core.io.AutoName` class."""

import unittest
import os.path


class AutoNameTests(unittest.TestCase):

    def tearDown(self):
        from jicbioimage.core.io import AutoName
        AutoName.count = 0
        AutoName.prefix_format = "{:d}_"
        AutoName.namespace = ""

    def test_count(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.count, 0)

    def test_directory(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.directory, None)

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

    def test_default_namespace(self):
        from jicbioimage.core.io import AutoName
        self.assertEqual(AutoName.namespace, "")

    def test_custom_namespace(self):
        from jicbioimage.core.io import AutoName
        AutoName.namespace = "strand1."
        self.assertEqual(AutoName.namespace, "strand1.")

    def test_name_callable(self):
        from jicbioimage.core.io import AutoName
        self.assertTrue(callable(AutoName.name))

    def test_name_logic(self):
        from jicbioimage.core.io import AutoName

        def no_transform(image):
            return image

        self.assertEqual(AutoName.name(no_transform), '1_no_transform')
        AutoName.directory = os.path.join('/', 'tmp')
        self.assertEqual(AutoName.name(no_transform),
                         os.path.join('/', 'tmp', '2_no_transform'))

    def test_custom_prefix_name_logic(self):
        from jicbioimage.core.io import AutoName
        AutoName.prefix_format = "{:02d}_"

        def no_transform(image):
            return image

        self.assertEqual(AutoName.name(no_transform), '01_no_transform')

    def test_custom_namespace_logic(self):
        from jicbioimage.core.io import AutoName
        AutoName.namespace = "strand1."

        def no_transform(image):
            return image

        self.assertEqual(AutoName.name(no_transform),
                         '1_strand1.no_transform')

if __name__ == '__main__':
    unittest.main()
