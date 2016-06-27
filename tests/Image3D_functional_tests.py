"""Image3D functional tests."""

import unittest
import os
import os.path
import shutil
import numpy as np

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, 'data')
TMP_DIR = os.path.join(HERE, 'tmp')


class Image3D_from_and_to_directory(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)

    def tearDown(self):
        shutil.rmtree(TMP_DIR)

    def test_to_directory(self):
        from jicbioimage.core.image import Image3D
        directory = os.path.join(TMP_DIR, "im3d")
        im3d = Image3D((50, 50, 10))
        im3d.to_directory(directory)

        expected = ["z0.png", "z1.png", "z2.png", "z3.png",
                    "z4.png", "z5.png", "z6.png", "z7.png",
                    "z8.png", "z9.png"]
        actual = os.listdir(directory)
        for f in expected:
            self.assertTrue(f in actual)

    def test_naming_with_two_digit_number(self):
        from jicbioimage.core.image import Image3D
        directory = os.path.join(TMP_DIR, "im3d")
        im3d = Image3D((50, 50, 11))
        im3d.to_directory(directory)

        expected = ["z00.png", "z01.png", "z02.png", "z03.png",
                    "z04.png", "z05.png", "z06.png", "z07.png",
                    "z08.png", "z09.png", "z10.png"]
        actual = os.listdir(directory)
        for f in expected:
            self.assertTrue(f in actual)

    def test_written_images_can_be_read(self):
        from jicbioimage.core.image import Image3D, Image
        directory = os.path.join(TMP_DIR, "im3d")

        z0 = np.zeros((50,50), dtype=np.uint8)
        z1 = np.ones((50, 50), dtype=np.uint8) * 255
        stack = np.dstack([z0, z1])
        im3d = Image3D.from_array(stack)
        im3d.to_directory(directory)

        im0 = Image.from_file(os.path.join(directory, "z0.png"))
        im1 = Image.from_file(os.path.join(directory, "z1.png"))

        self.assertTrue(np.array_equal(z0, im0))
        self.assertTrue(np.array_equal(z1, im1))

    def test_scaling_of_written_files(self):
        from jicbioimage.core.image import Image3D, Image
        directory = os.path.join(TMP_DIR, "im3d")

        z0 = np.zeros((50,50), dtype=np.uint8)
        z1 = np.ones((50, 50), dtype=np.uint8)

        stack = np.dstack([z0, z1])
        im3d = Image3D.from_array(stack)
        im3d.to_directory(directory)

        im0 = Image.from_file(os.path.join(directory, "z0.png"))
        im1 = Image.from_file(os.path.join(directory, "z1.png"))

        self.assertTrue(np.array_equal(z0, im0))
        self.assertTrue(np.array_equal(z1*255, im1))

        z2 = np.ones((50, 50), dtype=np.uint8) * 255

        stack = np.dstack([z0, z1, z2])
        im3d = Image3D.from_array(stack)
        im3d.to_directory(directory)

        im0 = Image.from_file(os.path.join(directory, "z0.png"))
        im1 = Image.from_file(os.path.join(directory, "z1.png"))
        im2 = Image.from_file(os.path.join(directory, "z2.png"))

        self.assertTrue(np.array_equal(z0, im0))
        self.assertTrue(np.array_equal(z1, im1))
        self.assertTrue(np.array_equal(z2*255, im1))
