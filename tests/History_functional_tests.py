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

    def test_apply_to(self):
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

        # This is the flow.
        red = red_channel(org_im)
        diff = channel_diff(red, green)

        # Apply the history.
        alt = diff.history.apply_to(org_im)

        # Creation statement from org_im.
        self.assertEqual(alt.history.creation,
                         org_im.history.creation)

        # Because it is the function within the transformation
        # function decorator that get's attached to the events
        # in the history of "diff" there the transformation
        # decorator is never accessed when calling "apply_to".
        # This means that no images get written out as events
        # are applied in the flow going from org_im to alt.
        # This also means that the history of alt is empty.
        self.assertEqual(len(alt.history), 0)

        # The transforms have been applied.
        np.array_equal(diff, alt)


if __name__ == '__main__':
    unittest.main()
