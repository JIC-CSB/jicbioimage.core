"""Tests for the :class:`jicbioimage.core.image.Image3D class."""

import unittest
import numpy as np

class ImageTests(unittest.TestCase):

    def test_import_Image3D_class(self):
        # This throws an error if the class cannot be imported.
        from jicbioimage.core.image import Image3D

    def test_instantiation_from_shape(self):
        from jicbioimage.core.image import Image3D
        image = Image3D((50, 50, 50))
        self.assertTrue(isinstance(image, np.ndarray))
        self.assertEqual(image.shape, (50, 50, 50))
        self.assertEqual(image.history[0],
                         'Instantiated Image3D from shape (50, 50, 50)')
