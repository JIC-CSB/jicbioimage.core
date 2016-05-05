import unittest

class ColorTests(unittest.TestCase):

    def test_import_color(self):

        from jicbioimage.core.util.color import pretty_color_from_identifier
        from jicbioimage.core.util.color import random_pretty_color

    def test_extract_8_bits(self):

        from jicbioimage.core.util.color import _extract_8_bits

        assert( _extract_8_bits(300) == 44 )
        assert( _extract_8_bits(300, 2) == 1 )

    def test_md5_hash_as_long(self):

        from jicbioimage.core.util.color import _md5_hash_as_long

        assert( _md5_hash_as_long(1) == \
                261578874264819908609102035485573088411 )

    def test_generate_rgb_tuple(self):

        from jicbioimage.core.util.color import (
            _generate_rgb_tuple,
            _md5_hash_as_long,
            _extract_8_bits)

        for identifier in range(1000):
            long_hash = _md5_hash_as_long(identifier)
            r, g, b = _generate_rgb_tuple(long_hash)

            assert( 0 <= b < 128 )
            assert( 128 <= g < 256 )
            assert( 0 <= r < 256 )

class PrettyColorUnitTests(unittest.TestCase):

    def test_generate_pretty_color(self):

        from jicbioimage.core.util.color import random_pretty_color

        generated_color = random_pretty_color()

        self.assertEqual(len(generated_color), 3)
        self.assertTrue(isinstance(generated_color, tuple))

        for _ in range(1000):
            generated_color = random_pretty_color()
            self.assertTrue(all(0 <= c <= 255 for c in generated_color))

    def test_pretty_with_identifier(self):

        from jicbioimage.core.util.color import pretty_color_from_identifier

        import random

        expected = (228, 90, 135)

        generated_color = pretty_color_from_identifier(0)
        self.assertEqual(generated_color, expected)


class PrettyColorPaletteUnitTests(unittest.TestCase):

    def test_import_pretty_color_palette(self):

        from jicbioimage.core.util.color import pretty_color_palette

    def test_pretty_color_palette(self):

        from jicbioimage.core.util.color import pretty_color_palette

        color_key = pretty_color_palette([0,1], keep_zero_black=False)
        self.assertEqual(len(color_key), 2)

        expected0 = (228, 90, 135)
        expected1 = (132, 27, 117)

        self.assertEqual(color_key[0], expected0)
        self.assertEqual(color_key[1], expected1)

    def test_pretty_color_palette_consistent(self):

        from jicbioimage.core.util.color import pretty_color_palette

        identifiers = range(1000)
        color_dict1 = pretty_color_palette(identifiers)
        color_dict2 = pretty_color_palette(identifiers)
        for i in identifiers:
            key = i
            self.assertEqual(color_dict1[key], color_dict2[key])

    def test_pretty_color_palette_exclude_zero(self):
        from jicbioimage.core.util.color import pretty_color_palette

        color_key = pretty_color_palette([0,1], keep_zero_black=True)
        self.assertEqual(len(color_key), 2)
        self.assertEqual(color_key[0], (0, 0, 0))

        expected = (132, 27, 117)

        self.assertEqual(color_key[0], (0, 0, 0))
        self.assertEqual(color_key[1], expected)


class UniqueColorUnitTests(unittest.TestCase):

    def test_unique_color_type(self):

        from jicbioimage.core.util.color import unique_color_from_identifier

        generated_color = unique_color_from_identifier(0)

        self.assertEqual(len(generated_color), 3)
        self.assertTrue(isinstance(generated_color, tuple))
        self.assertEqual(generated_color, (0, 0, 0))

        for i in generated_color:
            self.assertTrue(isinstance(i, int))

    def test_some_unique_colors(self):
        from jicbioimage.core.util.color import unique_color_from_identifier

        for i in range(1, 10):
            identifier = i
            blueish = unique_color_from_identifier(identifier)
            expected = (0, 0, i)
            self.assertEqual(blueish, expected)

            identifier = 256 + i
            greenish = unique_color_from_identifier(identifier)
            expected = (0, 1, i)
            self.assertEqual(greenish, expected)

            identifier = 256**2 + i
            redish = unique_color_from_identifier(identifier)
            expected = (1, 0, i)
            self.assertEqual(redish, expected)

    def test_unique_colors_edge_cases(self):
        from jicbioimage.core.util.color import unique_color_from_identifier
        self.assertEqual(unique_color_from_identifier(0), (0, 0, 0))
        self.assertEqual(unique_color_from_identifier(1), (0, 0, 1))
        self.assertEqual(unique_color_from_identifier(255), (0, 0, 255))
        self.assertEqual(unique_color_from_identifier(256), (0, 1, 0))
        self.assertEqual(unique_color_from_identifier(257), (0, 1, 1))
        self.assertEqual(unique_color_from_identifier(511), (0, 1, 255))
        self.assertEqual(unique_color_from_identifier(512), (0, 2, 0))
        self.assertEqual(unique_color_from_identifier(65536-1), (0, 255, 255))
        self.assertEqual(unique_color_from_identifier(65536), (1, 0, 0))
        self.assertEqual(unique_color_from_identifier(65536+1), (1, 0, 1))
        self.assertEqual(unique_color_from_identifier(65536+256), (1, 1, 0))
        self.assertEqual(unique_color_from_identifier(65536+256+1), (1, 1, 1))
        self.assertEqual(unique_color_from_identifier(16777215-256), (255, 254, 255))
        self.assertEqual(unique_color_from_identifier(16777215-1), (255, 255, 254))
        self.assertEqual(unique_color_from_identifier(16777215), (255, 255, 255))


    def test_non_in_raises_typerror(self):
        from jicbioimage.core.util.color import unique_color_from_identifier
        with self.assertRaises(TypeError):
            unique_color_from_identifier(1.)
        with self.assertRaises(TypeError):
            unique_color_from_identifier("1")

    def test_valid_range(self):
        from jicbioimage.core.util.color import unique_color_from_identifier
        with self.assertRaises(ValueError):
            unique_color_from_identifier(-1)
        with self.assertRaises(ValueError):
            unique_color_from_identifier(256*256*256)


class IdentifierFromUniqueColorUnitTests(unittest.TestCase):

    def test_identifier_from_unique_color(self):
        from jicbioimage.core.util.color import identifier_from_unique_color
        identifier = identifier_from_unique_color((0, 0, 0))
        self.assertEqual(identifier, 0)

    def test_identifier_from_unique_color_edge_cases(self):
        from jicbioimage.core.util.color import identifier_from_unique_color
        self.assertEqual(identifier_from_unique_color((0, 0, 0)), 0)
        self.assertEqual(identifier_from_unique_color((0, 0, 1)), 1)
        self.assertEqual(identifier_from_unique_color((0, 0, 255)), 255)
        self.assertEqual(identifier_from_unique_color((0, 1, 0)), 256)
        self.assertEqual(identifier_from_unique_color((0, 1, 1)), 257)
        self.assertEqual(identifier_from_unique_color((0, 1, 255)), 511)
        self.assertEqual(identifier_from_unique_color((0, 2, 0)), 512)
        self.assertEqual(identifier_from_unique_color((0, 255, 255)), 65536-1)
        self.assertEqual(identifier_from_unique_color((1, 0, 0)), 65536)
        self.assertEqual(identifier_from_unique_color((1, 0, 1)), 65536+1)
        self.assertEqual(identifier_from_unique_color((1, 1, 0)), 65536+256)
        self.assertEqual(identifier_from_unique_color((1, 1, 1)), 65536+256+1)
        self.assertEqual(identifier_from_unique_color((255, 254, 255)), 16777215-256)
        self.assertEqual(identifier_from_unique_color((255, 255, 254)), 16777215-1)
        self.assertEqual(identifier_from_unique_color((255, 255, 255)), 16777215)



if __name__ == '__main__':
	unittest.main()
