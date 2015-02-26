"""Module for managing and accessing images."""

import os
from collections import namedtuple
import tempfile
import json

class ImageProxy(object):
    """Image class."""

    def __init__(self, fpath):
        self.fpath = fpath

class ImageCollection(list):
    """Class for storing related images."""

    def parse_manifest(self, fpath):
        """Parse manifest file to build up the collection of images."""
        with open(fpath, 'r') as fh:
            for entry in json.load(fh):
                image_proxy = ImageProxy(entry["filename"])
                self.append(image_proxy)


class FileBackend(object):
    """Class for storing tiff files."""

    class Entry(object):
        """Class representing an entry in the backend."""
        def __init__(self, base_dir, fpath):
            fname = os.path.basename(fpath)
            self._directory = os.path.join(base_dir, fname)
            os.mkdir(self.directory)

        @property
        def directory(self):
            """Return the path to where the entry data is stored."""
            return self._directory

    def __init__(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self._directory = directory

    @property
    def directory(self):
        """Return the path to where the data is stored."""
        return self._directory

    def new_entry(self, fpath):
        """Return a new entry; to be populated with images."""
        return FileBackend.Entry(self.directory, fpath)


class _BFConvertWrapper(object):
    """Class for unpacking microscopy files using bfconvert."""

    def __init__(self, backend):
        self.backend = backend
        self.split_order = ['s', 'c', 'z', 't']

    @property
    def split_pattern(self):
        """Return pattern used to split the input file."""
        patterns = []
        for p in self.split_order:
            patterns.append('_{}%{}'.format(p.capitalize(), p))
        return ''.join(patterns)

    def manifest(self, entry):
        """Returns manifest as a Python list."""
        entries = []
        for fname in os.listdir(entry.directory):
            if fname == 'manifest.json':
                continue
            fpath = os.path.abspath(fname)
            metadata = self.metadata_from_fname(fname)
            entries.append({"filename": fpath,
                            "metadata": {"series": metadata.s,
                                         "channel": metadata.c,
                                         "zslice": metadata.z,
                                         "timepoint": metadata.t}})
        return entries

    def run_command(self, input_file, output_dir=None):
        """Return the command for running bfconvert."""
        base_name = os.path.basename(input_file)
        name, suffix = base_name.split('.', 1)
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

    def already_converted(self, fpath):
        """Return true if the file already has a manifest file in the backend."""
        manifest_fpath = os.path.join(self.backend.directory,
                                      os.path.basename(fpath),
                                      'manifest.json')
        return os.path.isfile(manifest_fpath)
        
    def __call__(self, input_file):
        """Run the convertion."""
        entry = self.backend.new_entry(input_file)
        cmd = self.run_command(input_file, entry.directory)
        os.system(cmd)
        manifest_fpath = os.path.join(entry.directory, 'manifest.json')
        with open(manifest_fpath, 'w') as fh:
            json.dump(self.manifest(entry), fh)
        return manifest_fpath

class DataManager(list):
    """Class for managing :class:`ImageCollection` instances."""

    def __init__(self, backend):
        self.backend = backend
        self.convert = _BFConvertWrapper(self.backend)

    def load(self, fpath):
        """Load a microscopy file."""
        if not self.convert.already_converted(fpath):
            path_to_manifest = self.convert(fpath) # unpacks and creates manifests
            image_collection = ImageCollection()
            image_collection.parse_manifest(path_to_manifest)
            self.append(image_collection)
