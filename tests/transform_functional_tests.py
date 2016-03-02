"""Transform functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class TransformationUserStory(unittest.TestCase):

    def setUp(self):
        from jicbioimage.core.io import AutoName
        AutoName.count = 0
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        from jicbioimage.core.io import AutoName
        AutoName.count = 0
        shutil.rmtree(TMP_DIR)

    def test_creating_transformations_from_scratch(self):

        # What if the default names of images was just the order in which they
        # were created?
        # Or perhaps the order + the function name, e.g.
        # 1_gaussian.png
        # 2_sobel.png
        # 3_gaussian.png
        # The order could be tracked in a class variable in an AutoName
        # object. The AutoName object could also store the output directory
        # as a class variable.

        from jicbioimage.core.image import Image
        from jicbioimage.core.transform import transformation
        from jicbioimage.core.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def identity(image):
            return image

        image = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))
        image = identity(image)
        self.assertEqual(len(image.history), 2, image.history)
        self.assertEqual(image.history[-1], 'Applied identity transform')
        created_fpath = os.path.join(TMP_DIR, '1_identity.png')
        self.assertTrue(os.path.isfile(created_fpath),
                        'No such file: {}'.format(created_fpath))

    def test_transform_can_take_named_argument(self):
        from jicbioimage.core.image import Image
        from jicbioimage.core.transform import transformation
        from jicbioimage.core.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def identity(image):
            return image

        image = Image((50, 50))

        # The command below should not raise an IndexError.
        image = identity(image=image)

    def test_BZ2(self):
        from skimage.filters import gaussian_filter

        from jicbioimage.core.image import Image
        from jicbioimage.core.transform import transformation
        from jicbioimage.core.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def blur(image):
            new_image = np.zeros(image.shape, dtype=np.float)
            sigma = 2
            if len(image.shape) == 3:
                # We have an RGB image.
                for i in range(image.shape[2]):
                    new_image[:][:][i] = gaussian_filter(image[:][:][i], sigma)
            else:
                new_image = gaussian_filter(image, sigma)
            return new_image

        image = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))

        # Image will have one item in history now.
        self.assertEqual(len(image.history), 1)
        self.assertTrue(image.history[0].startswith('Created image from'))

        image = blur(image)

        # Image should have two items in history now.
        self.assertEqual(len(image.history), 2)
        self.assertTrue(image.history[0].startswith('Created image from'))
        self.assertEqual(image.history[1], 'Applied blur transform')

        # Image returned is of jicbioimage.core.image.Image type.
        self.assertTrue(isinstance(image, Image))

        created_fpath = os.path.join(TMP_DIR, '1_blur.png')
        self.assertTrue(os.path.isfile(created_fpath),
                        'No such file: {}'.format(created_fpath))

    def test_stack_to_image_transform(self):
        from jicbioimage.core.image import Image
        from jicbioimage.core.io import DataManager, FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)

        from jicbioimage.core.transform import transformation
        from jicbioimage.core.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def average_projection(stack):
            xmax, ymax, zmax = stack.shape
            projection = np.sum(stack, axis=2, dtype=np.uint8) // zmax
            return projection

        data_manager.load(os.path.join(DATA_DIR, 'z-series.ome.tif'))
        microscopy_collection = data_manager[0]
        stack = microscopy_collection.zstack_array()

        image = average_projection(stack)
        self.assertTrue(isinstance(image, Image))

    def test_auto_safe_dtype(self):
        # AutoSave.auto_safe_type is True by default
        from jicbioimage.core.transform import transformation
        from jicbioimage.core.io import AutoName
        import numpy as np

        AutoName.directory = TMP_DIR

        def some_transform(image):
            return image

        decorated = transformation(some_transform)
        im = np.zeros((50, 50), dtype=np.uint64)

        decorated(im)
        created_fpath = os.path.join(TMP_DIR, '1_some_transform.png')
        self.assertTrue(os.path.isfile(created_fpath),
                        'No such file: {}'.format(created_fpath))


if __name__ == '__main__':
    unittest.main()
