"""Transform functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np
from skimage.io import imread, use_plugin

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class TransformationUserStory(unittest.TestCase):

    def setUp(self):
        from jicimagelib.io import AutoName
        AutoName.count = 0
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        from jicimagelib.io import AutoName
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

        from jicimagelib.image import Image
        from jicimagelib.transform import transformation
        from jicimagelib.io import AutoName
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

    def test_BZ2(self):
        from skimage.filters import gaussian_filter

        from jicimagelib.image import Image
        from jicimagelib.transform import transformation
        from jicimagelib.io import AutoName
        AutoName.directory = TMP_DIR

        @transformation
        def blur(image):
            sigma = 2
            if len(image.shape) == 3:
                # We have an RGB image.
                for i in range(image.shape[2]):
                    image[:][:][i] = gaussian_filter(image[:][:][i], sigma)
            else:
                image = gaussian_filter(image, sigma)
            return image

        image = Image.from_file(os.path.join(DATA_DIR, 'tjelvar.png'))
        image = blur(image)

        # Image returned is of jicimagelib.image.Image type.
        self.assertTrue(isinstance(image, Image))

        # Image returned contains the history.
        self.assertEqual(image.history[-1], 'Applied blur transform')

        created_fpath = os.path.join(TMP_DIR, '1_blur.png')
        self.assertTrue(os.path.isfile(created_fpath),
            'No such file: {}'.format(created_fpath))

    def test_stack_to_image_transform(self):
        from jicimagelib.image import DataManager
        from jicimagelib.io import FileBackend
        backend = FileBackend(TMP_DIR)
        data_manager = DataManager(backend)

        from jicimagelib.transform import transformation
        from jicimagelib.io import AutoName
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

    def test_auto_safe_dtype(self):
        # AutoSave.auto_safe_type is True by default
        from jicimagelib.transform import transformation
        from jicimagelib.io import AutoName
        import numpy as np

        AutoName.directory = TMP_DIR

        def some_transform(image):
            return image

        decorated = transformation(some_transform)
        im = np.zeros((50,50), dtype=np.uint64)

        decorated(im)
        created_fpath = os.path.join(TMP_DIR, '1_some_transform.png')
        self.assertTrue(os.path.isfile(created_fpath),
            'No such file: {}'.format(created_fpath))

class GeneralPurposeTransoformTests(unittest.TestCase):

    def setUp(self):
        from jicimagelib.io import AutoName
        AutoName.count = 0
        AutoName.directory = TMP_DIR
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        from jicimagelib.io import AutoName
        AutoName.count = 0
        shutil.rmtree(TMP_DIR)

    def test_max_intensity_projection(self):
        from jicimagelib.transform import max_intensity_projection
        from jicimagelib.image import Image
        slice0 = np.array(
            [[ 0, 1, 2],
             [ 0, 1, 2],
             [ 0, 1, 2]], dtype=np.uint8)
        slice1 = np.array(
            [[ 2, 1, 0],
             [ 2, 1, 0],
             [ 2, 1, 0]], dtype=np.uint8)
        expected = np.array(
            [[ 2, 1, 2],
             [ 2, 1, 2],
             [ 2, 1, 2]], dtype=np.uint8)
        stack = np.dstack([slice0, slice1])
        max_projection = max_intensity_projection(stack)
        self.assertTrue( np.array_equal(expected, max_projection) )
        self.assertTrue( isinstance(max_projection, Image) )
        
    def test_min_intensity_projection(self):
        from jicimagelib.transform import min_intensity_projection
        from jicimagelib.image import Image
        slice0 = np.array(
            [[ 0, 1, 2],
             [ 0, 1, 2],
             [ 0, 1, 2]], dtype=np.uint8)
        slice1 = np.array(
            [[ 2, 1, 0],
             [ 2, 1, 0],
             [ 2, 1, 0]], dtype=np.uint8)
        expected = np.array(
            [[ 0, 1, 0],
             [ 0, 1, 0],
             [ 0, 1, 0]], dtype=np.uint8)
        stack = np.dstack([slice0, slice1])
        min_projection = min_intensity_projection(stack)
        self.assertTrue( np.array_equal(expected, min_projection) )
        self.assertTrue( isinstance(min_projection, Image) )
        
    def test_smooth_gaussian(self):
        from jicimagelib.transform import smooth_gaussian
        from jicimagelib.image import Image
        array = np.array(
            [[ 0.,  0.,  0.],
             [ 0.,  1.,  0.],
             [ 0.,  0.,  0.]], dtype=np.float)
        expected = np.array(
            [[ 0.05855018,  0.09653293,  0.05855018],
             [ 0.09653293,  0.15915589,  0.09653293],
             [ 0.05855018,  0.09653293,  0.05855018]], dtype=np.float)
        smoothed = smooth_gaussian(array)
        self.assertTrue( np.allclose(expected, smoothed) )
        self.assertTrue( isinstance(smoothed, Image) )

        # The smooth_gaussian function only makes sense on dtype np.float.
        with self.assertRaises(TypeError):
            smoothed = smooth_gaussian(array.astype(np.uint8))

    def test_equalize_adaptive(self):
        from jicimagelib.transform import equalize_adaptive_clahe
        from jicimagelib.image import Image
        array = np.array(
            [[ 2., 2., 1., 1., 4., 4.],
             [ 2., 1., 1., 1., 1., 4.],
             [ 1., 1., 1., 1., 1., 1.],
             [ 1., 1., 1., 1., 1., 1.],
             [ 6., 1., 1., 1., 1., 8.],
             [ 6., 6., 1., 1., 8., 8.]], dtype=np.uint8)
        expected = np.array(
            [[ 1., 1., 0., 0., 1., 1.],
             [ 1., 0., 0., 0., 0., 1.],
             [ 0., 0., 0., 0., 0., 0.],
             [ 0., 0., 0., 0., 0., 0.],
             [ 1., 0., 0., 0., 0., 1.],
             [ 1., 1., 0., 0., 1., 1.]], dtype=np.float)
        equalised = equalize_adaptive_clahe(array, ntiles=2)
        print equalised
        self.assertTrue( np.array_equal(expected, equalised) )
        self.assertTrue( isinstance(equalised, Image) )

        # Cannot equalise an image with no variation.
        with self.assertRaises(RuntimeError):
            array = np.ones((6,6))
            equalised = equalize_adaptive_clahe(array, ntiles=2)

    def test_threshold_otsu(self):
        from jicimagelib.transform import threshold_otsu
        from jicimagelib.image import Image

        # Test with uint8.
        array = np.array(
            [[ 1,  2,  3],
             [ 7,  8,  9]], dtype=np.uint8)
        expected = np.array(
            [[ 0,  0,  0],
             [ 1,  1,  1]], dtype=np.bool)
        thresholded = threshold_otsu(array)
        self.assertTrue( np.array_equal(expected, thresholded) )
        self.assertTrue( isinstance(thresholded, Image) )

        # Test with float.
        array = np.array(
            [[ 1,  2,  3],
             [ 7,  8,  9]], dtype=np.float)
        expected = np.array(
            [[ 0,  0,  0],
             [ 1,  1,  1]], dtype=np.bool)
        thresholded = threshold_otsu(array)
        self.assertTrue( np.array_equal(expected, thresholded) )
        self.assertTrue( isinstance(thresholded, Image) )

    def test_threshold_otsu_multiplier(self):
        from jicimagelib.transform import threshold_otsu
        array = np.array(
            [[ 1,  2,  3],
             [ 7,  8,  9]], dtype=np.uint8)
        # Threshold used: 3 * 0.6 = 1.79
        expected = np.array(
            [[ 0,  1,  1],
             [ 1,  1,  1]], dtype=np.bool)
        thresholded = threshold_otsu(array, multiplier=0.6)
        self.assertTrue( np.array_equal(expected, thresholded) )

    def test_remove_small_objects(self):
        from jicimagelib.transform import remove_small_objects
        from jicimagelib.image import Image
        array = np.array(
            [[ 0,  0,  0, 0, 1],
             [ 0,  1,  1, 0, 0],
             [ 0,  1,  1, 0, 0],
             [ 0,  0,  0, 0, 1],
             [ 1,  1,  0, 1, 1]], dtype=np.bool)
        expected = np.array(
            [[ 0,  0,  0, 0, 0],
             [ 0,  1,  1, 0, 0],
             [ 0,  1,  1, 0, 0],
             [ 0,  0,  0, 0, 0],
             [ 0,  0,  0, 0, 0]], dtype=np.bool)
        no_small = remove_small_objects(array, min_size=4)
        self.assertTrue( np.array_equal(expected, no_small) )
        self.assertTrue( isinstance(no_small, Image) )

        # The smooth_gaussian function only makes sense on dtype np.bool.
        with self.assertRaises(TypeError):
            smoothed = remove_small_objects(array.astype(np.uint8))


if __name__ == '__main__':
    unittest.main()
