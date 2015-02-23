"""Module containing all classes related to loading and accessing images."""

import os.path
from collections import namedtuple

class _BFConvertDataManager(object):
    """Class for interfacing to bftools/bfconvert."""

    def __init__(self):
        self.split_order = ['s', 'c', 'z', 't']

    @property
    def split_pattern(self):
        """Return pattern used to split the input file."""
        patterns = []
        for p in self.split_order:
            patterns.append('_{}%{}'.format(p.capitalize(), p))
        return ''.join(patterns)

    def run_command(self, input_file, output_dir=None):
        """Return the command for running bfconvert."""
        base_name = os.path.basename(input_file)
        name, suffix = base_name.split('.')
        output_file = '{}{}.tif'.format(name, self.split_pattern)
        if output_dir:
            output_file = os.path.join(output_dir, output_file)
        return 'bfconvert {} {}'.format(input_file, output_file)

    def metadata_from_fname(self, fname):
        """Return meta data extracted from file name."""
        MetaData = namedtuple('MetaData', self.split_order)
        base_name = os.path.basename(fname)              # e.g. 'test_S1_C2_Z3_T4.tif'
        name, suffix = base_name.split('.')              # e.g. 'test_S1_C2_Z3_T4', 'tif'
        data = name.split('_')[-len(self.split_order):]  # e.g. ['S1', 'C2', 'Z3', 'T4']
        args = [ int(x[1]) for x in data ]               # e.g. [1, 2, 3, 4]
        return MetaData(*args)
        

        

class DataManager(object):
    """Manage :class:`jicimagelib.image.ImageCollection` instances."""

