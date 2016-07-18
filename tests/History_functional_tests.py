"""History functional tests."""

import unittest
import os
import os.path
import shutil

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class HistoryUserStory(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_storing_array_argument_as_string(self):
        import numpy as np
        from jicbioimage.core.image import Image
        from jicbioimage.core.transform import transformation
        from jicbioimage.core.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def red_channel(image):
            return image[:, :, 0]

        @transformation
        def green_channel(image):
            return image[:, :, 1]

        @transformation
        def channel_diff(im1, im2):
            return np.abs(im1 - im2)

        org_im = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))

        green = green_channel(org_im)
        red = red_channel(org_im)


        # Test with args.
        diff = channel_diff(red, green)
        last_event = diff.history[-1]
        self.assertEqual(last_event.args[0], repr(green))
        pos = hex(id(green))
        expected = """<History.Event(red_channel(image))>
<History.Event(channel_diff(image, '<Image object at {}, dtype=uint8>'))>""".format(pos)
        actual = "\n".join([str(e) for e in diff.history])
        self.assertEqual(actual, expected)

        # Test with kwargs.
        diff = channel_diff(red, im2=green)
        last_event = diff.history[-1]
        self.assertEqual(last_event.kwargs["im2"], repr(green))
        expected = """<History.Event(red_channel(image))>
<History.Event(channel_diff(image, im2='<Image object at {}, dtype=uint8>'))>""".format(pos)
        actual = "\n".join([str(e) for e in diff.history])
        self.assertEqual(actual, expected)


    def test_repr_with_int_arg(self):

        from jicbioimage.core.image import Image
        from jicbioimage.core.transform import transformation

        from jicbioimage.core.io import AutoName
        AutoName.directory = TMP_DIR

        image = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))
        image = image[:, :, 0]

        @transformation
        def threshold_abs(image, cutoff):
            """Return thresholded image."""
            return image > cutoff

        image = threshold_abs(image, 50)

        event = image.history[0]
        self.assertEqual(repr(event), "<History.Event(threshold_abs(image, 50))>")


if __name__ == '__main__':
    unittest.main()
