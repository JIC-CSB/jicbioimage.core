"""Unit tests for jicbioimage.core.io module."""

import unittest
import os

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

class sorted_listdir_test(unittest.TestCase):

    @patch('os.listdir')
    def test_sorted_lisdir(self, patch_listdir):
        patch_listdir.return_value = ["z20.png", "z3.png", "z1.png"]
        from jicbioimage.core.io import sorted_listdir
        l = sorted_listdir(".")
        patch_listdir.assert_called_with(".")
        self.assertEqual(l, ["z1.png", "z3.png", "z20.png"])
