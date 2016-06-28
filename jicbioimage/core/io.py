"""Module for reading and writing images."""

import sys
import os
import os.path
import subprocess
import json
from collections import namedtuple
import hashlib

from jicbioimage.core.image import (
    _sorted_listdir,
    ImageCollection,
    MicroscopyCollection,
)


def _md5_hexdigest_from_file(fpath, blocksize=65536):
    """Return md5 hex digest of a file."""
    md5_hash = hashlib.md5()
    with open(fpath, "rb") as fh:
        buf = fh.read(blocksize)
        while len(buf) > 0:
            md5_hash.update(buf)
            buf = fh.read(blocksize)
        return md5_hash.hexdigest()


class AutoName(object):
    """Class for generating output file names automatically."""
    count = 0
    directory = None  #: Output directory to save images to.
    prefix_format = "{:d}_"  #: Image file prefix format.
    namespace = ""  #: Image file namespace.

    @classmethod
    def prefix(cls):
        """Return auto generated file prefix."""
        return cls.prefix_format.format(cls.count)

    @classmethod
    def name(cls, func):
        """Return auto generated file name."""
        cls.count = cls.count + 1
        fpath = '{}{}{}'.format(cls.prefix(), cls.namespace,
                                  func.__name__)
        if cls.directory:
            fpath = os.path.join(cls.directory, fpath)
        return fpath


class AutoWrite(object):
    """Class for writing images automatically."""

    #: Whether or not auto writing of images is enabled.
    on = True


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
            md5 = _md5_hexdigest_from_file(fpath)
            self._directory = os.path.join(base_dir, md5)
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

    def split_pattern(self, win32=False):
        """Pattern used to split the input file."""
        patterns = []
        for p in self.split_order:
            if win32:
                patterns.append('{}%%{}'.format(p.capitalize(), p))
            else:
                patterns.append('{}%{}'.format(p.capitalize(), p))
        return '_'.join(patterns)

    def manifest(self, entry):
        """Returns manifest as a list.

        :param entry: :class:`jicbioimage.core.image.FileBackend.Entry`
        :returns: list
        """
        entries = []
        for fname in _sorted_listdir(entry.directory):
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
        output_file = '{}.tif'.format(self.split_pattern())
        bfconvert = 'bfconvert'
        if sys.platform == 'win32':
            bfconvert = 'bfconvert.bat'
            output_file = '{}.tif'.format(self.split_pattern(win32=True))
        if output_dir:
            output_file = os.path.join(output_dir, output_file)
        return [bfconvert, input_file, output_file]

    def metadata_from_fname(self, fname):
        """Return meta data extracted from file name.

        :param fname: metadata file name
        :returns: dynamically created :class:`collections.namedtuple`
        """
        MetaData = namedtuple('MetaData', self.split_order)

        base_name = os.path.basename(fname)
        # e.g. 'S1_C2_Z3_T4.tif'

        name, suffix = base_name.split('.')
        # e.g. 'S1_C2_Z3_T4', 'tif'

        data = name.split('_')
        # e.g. ['S1', 'C2', 'Z3', 'T4']

        args = [int(x[1:]) for x in data]
        # e.g. [1, 2, 3, 4]

        return MetaData(*args)

    def already_converted(self, fpath):
        """Return true if the file already has a manifest file in the backend.

        :param fpath: potential path to the manifest file
        :returns: bool
        """
        manifest_fpath = os.path.join(self.backend.directory,
                                      _md5_hexdigest_from_file(fpath),
                                      'manifest.json')
        return os.path.isfile(manifest_fpath)

    def __call__(self, input_file):
        """Run the conversion.

        Unpacks the microscopy file and creates the manifest file.

        :param input_file: path to the microscopy file
        :raises: RuntimeError
        :returns: path to manifest file
        """
        entry = self.backend.new_entry(input_file)
        cmd = self.run_command(input_file, entry.directory)
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stderr = p.stderr.read()
        except OSError as e:
            msg = 'bfconvert tool not found in PATH\n{}'.format(e)
            raise(RuntimeError(msg))
        if len(stderr) > 0:
            raise(RuntimeError(stderr))
        manifest_fpath = os.path.join(entry.directory, 'manifest.json')
        with open(manifest_fpath, 'w') as fh:
            json.dump(self.manifest(entry), fh)
        return manifest_fpath


class DataManager(list):
    """Manage :class:`jicbioimage.core.image.ImageCollection` instances."""

    def __init__(self, backend=None):
        if backend is None:
            dirpath = os.path.join(os.getcwd(), 'jicbioimage.core_backend')
            backend = FileBackend(directory=dirpath)
        self.backend = backend
        self.convert = BFConvertWrapper(self.backend)

    def load(self, fpath):
        """Load a microscopy file.

        :param fpath: path to microscopy file
        """
        def is_microscopy_item(fpath):
            """Return True if the fpath is likely to be microscopy data.

            :param fpath: file path to image
            :returns: :class:`bool`
            """
            l = fpath.split('.')
            ext = l[-1]
            pre_ext = l[-2]
            if ((ext == 'tif' or ext == 'tiff')
               and pre_ext != 'ome'):
                return False
            return True

        if not self.convert.already_converted(fpath):
            path_to_manifest = self.convert(fpath)
        else:
            path_to_manifest = os.path.join(self.backend.directory,
                                            _md5_hexdigest_from_file(fpath),
                                            'manifest.json')

        collection = None
        if is_microscopy_item(fpath):
            collection = MicroscopyCollection(path_to_manifest)
        else:
            collection = ImageCollection(path_to_manifest)
        self.append(collection)

        return collection
