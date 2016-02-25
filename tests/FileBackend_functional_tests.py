"""FileBackend functional tests."""

import unittest
import os
import os.path
import shutil

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')

class FileBackendBugs(unittest.TestCase):
    
    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_BZ1(self):
        """
        If the file backend creates a directory into which to unpack TIFFs, but
        then fails for some reason (e.g. bfconvert is not in the path), it has
        created a directory, but not a manifest. At this point, re-running the
        unpack fails because the directory already exists, and:
        os.mkdir(self.directory) throws an error.
        """
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(directory=TMP_DIR)
        data_manager = DataManager(backend=backend)
        fname = 'single-channel.ome.tif'

        # The directory already exists.
        os.mkdir(os.path.join(TMP_DIR, fname))

        # The below throws if the bug is present.
        data_manager.load(os.path.join(DATA_DIR, fname))

if __name__ == '__main__':
    unittest.main()
