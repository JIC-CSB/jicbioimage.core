"""Tests for the :class:`jicimagelib.image.MicroscopyImage` class."""

import unittest

class MicroscopyImage(unittest.TestCase):
    
    def test_instantiation(self):
        from jicimagelib.image import MicroscopyImage
        microscopy_image = MicroscopyImage('dummy.tif',
            dict(series=0, channel=1, zslice=2, timepoint=3))
        self.assertEqual(microscopy_image.fpath, 'dummy.tif')
        self.assertEqual(microscopy_image.series, 0)
        self.assertEqual(microscopy_image.channel, 1)
        self.assertEqual(microscopy_image.zslice, 2)
        self.assertEqual(microscopy_image.timepoint, 3)

    def test_is_me(self):
        from jicimagelib.image import MicroscopyImage
        microscopy_image = MicroscopyImage('dummy.tif',
            dict(series=0, channel=1, zslice=2, timepoint=3))
        self.assertTrue(microscopy_image.is_me(s=0, c=1, z=2, t=3))
        self.assertFalse(microscopy_image.is_me(s=5, c=1, z=2, t=3))

    def test_in_zstack(self):
        from jicimagelib.image import MicroscopyImage
        microscopy_image = MicroscopyImage('dummy.tif',
            dict(series=0, channel=1, zslice=2, timepoint=3))
        self.assertTrue(microscopy_image.in_zstack(s=0, c=1, t=3))
        self.assertFalse(microscopy_image.in_zstack(s=5, c=1, t=3))

    def test_repr(self):
        from jicimagelib.image import MicroscopyImage
        microscopy_image = MicroscopyImage('dummy.tif',
            dict(series=0, channel=1, zslice=2, timepoint=3))
        self.assertEqual(repr(microscopy_image),
            '<MicroscopyImage(s=0, c=1, z=2, t=3) object at {}>'.format(
                hex(id(microscopy_image)))
        ) 


if __name__ == '__main__':
    unittest.main()
