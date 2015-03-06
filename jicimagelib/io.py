"""Module for reading and writing images."""

import os.path

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

    
