"""Module for managing and accessing images."""

import os
import os.path
import subprocess
from collections import namedtuple
import json
import re
import numpy as np
from skimage.io import imread, use_plugin

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


#############################################################################
# Conversion classes for unpacking microscopy data.
#############################################################################

class _BFConvertWrapper(object):
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
                            "metadata": {"series": metadata.s,
                                         "channel": metadata.c,
                                         "zslice": metadata.z,
                                         "timepoint": metadata.t}})
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


#############################################################################
# Classes for managing image data.
#############################################################################

class Image(np.ndarray):
    """Image class."""

    @classmethod
    def from_array(cls, array, name=None):
        """Return :class:`jicimagelib.image.Image` instance from an array.
        
        :param array: :class:`numpy.ndarray`
        :param name: name of the image
        :returns: :class:`jicimagelib.image.Image`
        """
        image = array.view(cls)
        event = 'Created image from array'
        if name:
            event = '{} as {}'.format(event, name)
        image.history.append(event)
        return image
        
    @classmethod
    def from_file(cls, fpath, name=None, format=None):
        """Return :class:`jicimagelib.image.Image` instance from a file.
        
        :param fpath: path to the image file
        :param name: name of the image
        :param format: file format of the image file
        :returns: :class:`jicimagelib.image.Image`
        """
        use_plugin('freeimage')
        ar = imread(fpath)

        # Create a :class:`jicimagelib.image.Image` instance.
        image = Image.from_array(ar, name)

        # Reset history, as image is created from file not array.
        image.history = []
        event = 'Created image from {}'.format(fpath)
        if name:
            event = '{} as {}'.format(event, name)
        image.history.append(event)

        return image


        

    def __new__(subtype, shape, dtype=np.uint8, buffer=None, offset=0,
                 strides=None, order=None, name=None):
        obj = np.ndarray.__new__(subtype, shape, dtype, buffer, offset,
                                 strides, order)
        obj.name = name
        obj.history = []
        return obj

    def __init__(self, shape, dtype=np.uint8, buffer=None, offset=0,
                 strides=None, order=None, name=None):
        event = 'Instantiated image from shape {}'.format(shape)
        if name:
            event = '{} as {}'.format(event, name)
        self.history.append(event)
        
    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.name = getattr(obj, 'name', None)
        self.history = getattr(obj, 'history', [])

class ImageProxy(object):
    """Lightweight image class."""

    def __init__(self, fpath, s, c, z, t):
        self.fpath = fpath
        self.series = s
        self.channel = c
        self.zslice = z
        self.timepoint = t

    @property
    def image(self):
        """Underlying :class:`jicimagelib.image.Image` instance."""
        return Image.from_file(self.fpath)

class ImageCollection(list):
    """Class for storing related images."""

    def parse_manifest(self, fpath):
        """Parse manifest file to build up the collection of images.
        
        :param fpath: path to the manifest file
        """
        with open(fpath, 'r') as fh:
            for entry in json.load(fh):
                image_proxy = ImageProxy(entry["filename"],
                                         s=entry["metadata"]["series"],
                                         c=entry["metadata"]["channel"],
                                         z=entry["metadata"]["zslice"],
                                         t=entry["metadata"]["timepoint"])
                self.append(image_proxy)

    def image_proxy(self, s=0, c=0, z=0, t=0):
        """Return a :class:`jicimagelib.image.ImageProxy` instance.
        
        :param s: series
        :param c: channel
        :param z: zslice
        :param t: timepoint
        :returns: :class:`jicimagelib.image.ImageProxy`
        """
        for image_proxy in self:
            if (image_proxy.series == s
                and image_proxy.channel == c
                and image_proxy.zslice == z
                and image_proxy.timepoint == t):
                return image_proxy

    def zstack_proxy_iterator(self, s=0, c=0, t=0):
        """Return iterator of :class:`jicimagelib.image.ImageProxy` instances in the zstack.
        
        :param s: series
        :param c: channel
        :param t: timepoint
        :returns: zstack :class:`jicimagelib.image.ImageProxy` iterator
        """
        for image_proxy in self:
            if (image_proxy.series == s
                and image_proxy.channel == c
                and image_proxy.timepoint == t):
                yield image_proxy

    def zstack_array(self, s=0, c=0, t=0):
        """Return zstack as a :class:`numpy.ndarray`.
        
        :param s: series
        :param c: channel
        :param t: timepoint
        :returns: zstack as a :class:`numpy.ndarray`
        """
        return np.dstack([x.image for x in self.zstack_proxy_iterator(s=s, c=c, t=t)])

    def image(self, s=0, c=0, z=0, t=0):
        """Return image as a :class:`jicimagelib.image.Image`.
        
        :param s: series
        :param c: channel
        :param z: zslice
        :param t: timepoint
        :returns: :class:`jicimagelib.image.Image`
        """
        return self.image_proxy(s=s, c=c, z=z, t=t).image


class DataManager(list):
    """Class for managing :class:`jicimagelib.image.ImageCollection` instances."""

    def __init__(self, backend):
        self.backend = backend
        self.convert = _BFConvertWrapper(self.backend)

    def load(self, fpath):
        """Load a microscopy file.
        
        :param fpath: path to microscopy file
        """
        if not self.convert.already_converted(fpath):
            path_to_manifest = self.convert(fpath)
        else:
            path_to_manifest = os.path.join(self.backend.directory,
                                            os.path.basename(fpath),
                                            'manifest.json')

        image_collection = ImageCollection()
        image_collection.parse_manifest(path_to_manifest)
        self.append(image_collection)

            
