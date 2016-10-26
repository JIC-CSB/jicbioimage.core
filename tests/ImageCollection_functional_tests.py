"""ImageCollectionImage functional tests."""

import unittest
import os
import os.path
import shutil
import json

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class ImageCollectionUserStory(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_parse_manifest_raises_runtime_error_if_no_filename(self):
        # Create manifest.json file without fpath.
        manifest_fp = os.path.join(TMP_DIR, 'manifest.json')
        with open(manifest_fp, 'w') as fh:
            json.dump({"nofpath": "/tmp"}, fh)

        from jicbioimage.core.image import ImageCollection
        image_collection = ImageCollection()
        with self.assertRaises(RuntimeError):
            image_collection.parse_manifest(manifest_fp)

    def test_parse_manifest_raises_backwards_compatible_with_abs_paths(self):
        # Create manifest.json file without fpath.
        manifest_fp = os.path.join(TMP_DIR, 'manifest.json')
        shutil.copy(os.path.join(DATA_DIR, "tjelvar.png"), TMP_DIR)
        abs_im_fpath = os.path.join(TMP_DIR, 'tjelvar.png')
        entry = dict(filename=abs_im_fpath, series=0, channel=0, zslice=0,
                     timepoint=0)
        with open(manifest_fp, 'w') as fh:
            json.dump([entry], fh)

        from jicbioimage.core.image import ImageCollection, Image
        image_collection = ImageCollection()
        image_collection.parse_manifest(manifest_fp)
        im = image_collection[0].image
        expected_im = Image.from_file(abs_im_fpath)
        import numpy as np
        self.assertTrue(np.array_equal(im, expected_im))

if __name__ == '__main__':
    unittest.main()
