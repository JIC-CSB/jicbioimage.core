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

    
