"""Module for reading and writing images."""

import os
import os.path
import re
import tempfile
import subprocess
import json
from collections import namedtuple

class TemporaryFilePath(object):
    """Temporary file path context manager."""
    def __init__(self, suffix):
        self.suffix = suffix

    def __enter__(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix=self.suffix, delete=False)
        self.fpath = tmp_file.name
        tmp_file.close()
        return self

    def __exit__(self, type, value, tb):
        os.unlink(self.fpath)

class AutoName(object):
    """Class for generating output file names automatically."""
    count = 0
    directory = None  #: Output directory to save images to.
    suffix = '.png'   #: Image file suffix.
    
    @classmethod
    def name(cls, func):
        """Return auto generated file name.""" 
        cls.count = cls.count + 1
        fpath = '{}_{}{}'.format(cls.count, func.__name__, cls.suffix)
        if cls.directory:
            fpath = os.path.join(cls.directory, fpath)
        return fpath
            
class AutoWrite(object):
    """Class for writing images automatically."""

    #: Whether or not auto writing of images is enabled.
    on = True

    #: Ensure image to be written has a safe dtype for writing to file.
    auto_safe_dtype = True

    
#############################################################################
# Back ends classes for storing/caching unpacked microscopy images.
#############################################################################

class FileBackend(object):
    """Class for storing image files."""

    class Entry(object):
        """Class representing a backend entry."""
        def __init__(self, base_dir, fpath):
            """Initialise a new entry; to be populated with images.

            The base name of the fpath argument is used to create a
            subdirectory in the backend directory specific for the microscopy
            file to be loaded.

            :param base_dir: backend directory
            :param fpath: path to the microscopy image of interest
            """
            fname = os.path.basename(fpath)
            self._directory = os.path.join(base_dir, fname)
            if not os.path.isdir(self.directory):
                os.mkdir(self.directory)

        @property
        def directory(self):
            """Where the images are stored."""
            return self._directory

    def __init__(self, directory):
        """Initialise a backend.

        Creates the backend directory if it does not already exist.

        :param directory: location of the backend
        """
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self._directory = directory

    @property
    def directory(self):
        """Where the entries are stored."""
        return self._directory

    def new_entry(self, fpath):
        """Return a new entry; to be populated with images.

        :param fpath: path to microscopy image
        :returns: :class:`jiciimagelib.image.FileBackend.Entry` instance
        """
        return FileBackend.Entry(self.directory, fpath)


class BFConvertWrapper(object):
    """Class for unpacking microscopy files using bfconvert."""

    def __init__(self, backend):
        self.backend = backend
        self.split_order = ['s', 'c', 'z', 't']

    @property
    def split_pattern(self):
        """Pattern used to split the input file."""
        patterns = []
        for p in self.split_order:
            patterns.append('_{}%{}'.format(p.capitalize(), p))
        return ''.join(patterns)

    def _sorted_nicely(self, l):
        """Return list sorted in the way that humans expect.
        
        :param l: iterable to be sorted
        :returns: sorted list
        """
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(l, key = alphanum_key)

    def manifest(self, entry):
        """Returns manifest as a list.
        
        :param entry: :class:`jicimagelib.image.FileBackend.Entry`
        :returns: list
        """
        entries = []
        for fname in self._sorted_nicely(os.listdir(entry.directory)):
            if fname == 'manifest.json':
                continue
            fpath = os.path.abspath(os.path.join(entry.directory, fname))
            metadata = self.metadata_from_fname(fname)
            entries.append({"filename": fpath,
                            "series": metadata.s,
                            "channel": metadata.c,
                            "zslice": metadata.z,
                            "timepoint": metadata.t})
        return entries

    def run_command(self, input_file, output_dir=None):
        """Return the command for running bfconvert as a list.
        
        :param input_file: path to microscopy image to be converted
        :param ouput_dir: directory to write output tiff files to
        :returns: list
        """
        base_name = os.path.basename(input_file)
        name, suffix = base_name.split('.', 1)
        output_file = '{}{}.tif'.format(name, self.split_pattern)
        if output_dir:
            output_file = os.path.join(output_dir, output_file)
        return ['bfconvert', input_file, output_file]

    def metadata_from_fname(self, fname):
        """Return meta data extracted from file name.
        
        :param fname: metadata file name
        :returns: dynamically created :class:`collections.namedtuple`
        """
        MetaData = namedtuple('MetaData', self.split_order)
        base_name = os.path.basename(fname)              # e.g. 'test_S1_C2_Z3_T4.tif'
        name, suffix = base_name.split('.')              # e.g. 'test_S1_C2_Z3_T4', 'tif'
        data = name.split('_')[-len(self.split_order):]  # e.g. ['S1', 'C2', 'Z3', 'T4']
        args = [ int(x[1:]) for x in data ]               # e.g. [1, 2, 3, 4]
        return MetaData(*args)

    def already_converted(self, fpath):
        """Return true if the file already has a manifest file in the backend.
        
        :param fpath: potential path to the manifest file
        :returns: bool
        """
        manifest_fpath = os.path.join(self.backend.directory,
                                      os.path.basename(fpath),
                                      'manifest.json')
        return os.path.isfile(manifest_fpath)
        
    def __call__(self, input_file):
        """Run the conversion.
        
        Unpacks the microscopy file and creates the manifest file.

        :param input_file: path to the microscopy file
        :returns: path to manifest file
        """
        entry = self.backend.new_entry(input_file)
        cmd = self.run_command(input_file, entry.directory)
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stderr = p.stderr.read()
        except OSError:
            raise(RuntimeError('bfconvert tool not found in PATH'))
        if len(stderr) > 0:
            raise(RuntimeError(stderr))
        manifest_fpath = os.path.join(entry.directory, 'manifest.json')
        with open(manifest_fpath, 'w') as fh:
            json.dump(self.manifest(entry), fh)
        return manifest_fpath


