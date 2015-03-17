"""Module for managing and accessing images."""

import os
import os.path
import json
import numpy as np
from skimage.io import imread, imsave, use_plugin

from jicimagelib.io import (
    TemporaryFilePath,
    BFConvertWrapper,
)


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
    def from_file(cls, fpath, name=None):
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

    @property
    def png(self):
        """Return png string of image."""
        use_plugin('freeimage')
        with TemporaryFilePath(suffix='.png') as tmp:
            imsave(tmp.fpath, self)
            with open(tmp.fpath, 'rb') as fh:
                return fh.read()


    def _repr_png_(self):
        """Return image as png string.

        Used by IPython qtconsole/notebook to display images.
        """
        return self.png

class ProxyImage(object):
    """Lightweight image class."""

    def __init__(self, fpath, metadata={}):
        self.fpath = fpath
        for key, value in metadata.items():
            self.__setattr__(key, value)

    @property
    def image(self):
        """Underlying :class:`jicimagelib.image.Image` instance."""
        return Image.from_file(self.fpath)

    def _repr_png_(self):
        """Return image as png string.

        Used by IPython qtconsole/notebook to display images.
        """
        return self.image.png

class MicroscopyImage(ProxyImage):
    """Lightweight image class with microscopy meta data."""

    def is_me(self, s, c, z, t):
        """Return True if arguments match my meta data.

        :param s: series
        :param c: channel
        :param z: zslice
        :param t: timepoint
        :returns: :class:`bool`
        """
        if (self.series == s
            and self.channel == c
            and self.zslice == z
            and self.timepoint == t):
            return True
        return False

    def in_zstack(self, s, c, t):
        """Return True if I am in the zstack.

        :param s: series
        :param c: channel
        :param t: timepoint
        :returns: :class:`bool`
        """
        if (self.series == s
            and self.channel == c
            and self.timepoint == t):
            return True
        return False

class ImageCollection(list):
    """Class for storing related images."""

    def proxy_image(self, index=0):
        """Return a :class:`jicimagelib.image.ProxyImage` instance.
        
        :param index: list index
        :returns: :class:`jicimagelib.image.ProxyImage`
        """
        return self[index]

    def image(self, index=0):
        """Return image as a :class:`jicimagelib.image.Image`.
        
        :param index: list index
        :returns: :class:`jicimagelib.image.Image`
        """
        return self.proxy_image(index=index).image

    def parse_manifest(self, fpath):
        """Parse manifest file to build up the collection of images.
        
        :param fpath: path to the manifest file
        """
        with open(fpath, 'r') as fh:
            for entry in json.load(fh):

                # Every entry of a manifest file needs to have a "filename"
                # attribute. It is the only requirement so we check for it in a
                # strict fashion.
                if "filename" not in entry:
                    raise(RuntimeError(
                        'Entries in {} need to have "filename"'.format(fpath)))

                filename = entry.pop("filename")

                proxy_image = None
                if isinstance(self, MicroscopyCollection):
                    proxy_image = MicroscopyImage(filename, entry)
                else:
                    proxy_image = ProxyImage(filename, entry)
                self.append(proxy_image)

class MicroscopyCollection(ImageCollection):
    """Class for storing related :class:`jicimagelib.image.MicroscopyImage` instances."""

    def proxy_image(self, s=0, c=0, z=0, t=0):
        """Return a :class:`jicimagelib.image.MicroscopyImage` instance.
        
        :param s: series
        :param c: channel
        :param z: zslice
        :param t: timepoint
        :returns: :class:`jicimagelib.image.MicroscopyImage`
        """
        for proxy_image in self:
            if proxy_image.is_me(s=s, c=c, z=z, t=t):
                return proxy_image

    def zstack_proxy_iterator(self, s=0, c=0, t=0):
        """Return iterator of :class:`jicimagelib.image.ProxyImage` instances in the zstack.
        
        :param s: series
        :param c: channel
        :param t: timepoint
        :returns: zstack :class:`jicimagelib.image.ProxyImage` iterator
        """
        for proxy_image in self:
            if proxy_image.in_zstack(s=s, c=c, t=t):
                yield proxy_image

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
        return self.proxy_image(s=s, c=c, z=z, t=t).image

class DataManager(list):
    """Class for managing :class:`jicimagelib.image.ImageCollection` instances."""

    def __init__(self, backend):
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
            if ( (ext == 'tif' or ext == 'tiff')
                and pre_ext != 'ome' ):
                return False
            return True

        if not self.convert.already_converted(fpath):
            path_to_manifest = self.convert(fpath)
        else:
            path_to_manifest = os.path.join(self.backend.directory,
                                            os.path.basename(fpath),
                                            'manifest.json')

        
        collection = None
        if is_microscopy_item(fpath):
            collection = MicroscopyCollection()
        else:
            collection = ImageCollection()
        collection.parse_manifest(path_to_manifest)
        self.append(collection)

        return collection

            
