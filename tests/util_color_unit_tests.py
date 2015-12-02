import unittest

class ColorTests(unittest.TestCase):

    def test_import_color(self):

        from jicbioimage.core.util.color import pretty_color

    def test_extract_8_bits(self):

        from jicbioimage.core.util.color import _extract_8_bits

        assert( _extract_8_bits(300) == 44 )
        assert( _extract_8_bits(300, 2) == 1 )

    def test_md5_hash_as_long(self):

        from jicbioimage.core.util.color import _md5_hash_as_long

        assert( _md5_hash_as_long(1) == \
                261578874264819908609102035485573088411L )

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

        from jicbioimage.core.util.color import pretty_color

        generated_color = pretty_color()

        self.assertEqual(len(generated_color), 3)
        self.assertTrue(isinstance(generated_color, tuple))

        for _ in range(1000):
            generated_color = pretty_color()
            self.assertTrue(all(0 <= c <= 255 for c in generated_color))
    
    def test_pretty_with_identifier(self):

        from jicbioimage.core.util.color import pretty_color

        import random

        expected = (228, 90, 135)

        generated_color = pretty_color(0)
        self.assertEqual(generated_color, expected)

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
        
if __name__ == '__main__':
	unittest.main()    