"""Module for reading and writing images."""

import os
import os.path
import tempfile

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
    directory = None
    suffix = '.png'
    
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

