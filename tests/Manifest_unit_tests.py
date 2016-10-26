"""Unit tests for :class:`jicbioimage.core.io.Manifest."""

import unittest


class ManifestUnitTests(unittest.TestCase):

    def test_initialisation(self):
        from jicbioimage.core.io import Manifest
        manifest = Manifest()
        self.assertTrue(isinstance(manifest, list))

    def test_add_entry(self):
        from jicbioimage.core.io import Manifest
        manifest = Manifest()
        self.assertEqual(len(manifest), 0)
        entry = manifest.add(filename="my_image.png")
        self.assertEqual(len(manifest), 1)
        self.assertTrue(isinstance(entry, dict))
        self.assertEqual(entry["filename"], "my_image.png")

    def test_add_entry_with_custom_params(self):
        from jicbioimage.core.io import Manifest
        manifest = Manifest()
        self.assertEqual(len(manifest), 0)
        entry = manifest.add(filename="my_image.png", series=0)
        self.assertEqual(len(manifest), 1)
        self.assertTrue(isinstance(entry, dict))
        self.assertEqual(entry["filename"], "my_image.png")
        self.assertEqual(entry["series"], 0)

    def test_json(self):
        from jicbioimage.core.io import Manifest
        manifest = Manifest()
        manifest.add(filename="my_image.png", series=0)
        self.assertEqual(manifest.json,
                         '[{"filename": "my_image.png", "series": 0}]')
