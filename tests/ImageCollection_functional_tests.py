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
        
if __name__ == '__main__':
    unittest.main()
