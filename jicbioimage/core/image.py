"""Module for managing and accessing images."""

import os
import os.path
import json
import base64

import numpy as np
import scipy.ndimage
import skimage.io

from jicbioimage.core.io import (
    FileBackend,
    TemporaryFilePath,
    BFConvertWrapper,
)

from jicbioimage.core.util.array import normalise, false_color

from jicbioimage.core.region import Region

class Image(np.ndarray):
    """Image class."""

    @classmethod
    def from_array(cls, array, name=None, log_in_history=True):
        """Return :class:`jicbioimage.core.image.Image` instance from an array.
        
        :param array: :class:`numpy.ndarray`
        :param name: name of the image
        :param log_in_history: whether or not to log the creation event
                               in the image's history
        :returns: :class:`jicbioimage.core.image.Image`
        """
        image = array.view(cls)
        event = 'Created image from array'
        if name:
            event = '{} as {}'.format(event, name)
        if log_in_history:
            image.history.append(event)
        return image
        
    @classmethod
    def from_file(cls, fpath, name=None, log_in_history=True):
        """Return :class:`jicbioimage.core.image.Image` instance from a file.
        
        :param fpath: path to the image file
        :param name: name of the image
        :param log_in_history: whether or not to log the creation event
                               in the image's history
        :returns: :class:`jicbioimage.core.image.Image`
        """
        skimage.io.use_plugin('freeimage')
        ar = skimage.io.imread(fpath)

        # Create a :class:`jicbioimage.core.image.Image` instance.
        image = Image.from_array(ar, name)

        # Reset history, as image is created from file not array.
        image.history = []
        event = 'Created image from {}'.format(fpath)
        if name:
            event = '{} as {}'.format(event, name)
        if log_in_history:
            image.history.append(event)

        return image

    def __new__(subtype, shape, dtype=np.uint8, buffer=None, offset=0,
                 strides=None, order=None, name=None, log_in_history=True):
        obj = np.ndarray.__new__(subtype, shape, dtype, buffer, offset,
                                 strides, order)
        obj.name = name
        obj.history = []
        return obj

    def __init__(self, shape, dtype=np.uint8, buffer=None, offset=0,
                 strides=None, order=None, name=None, log_in_history=True):
        event = 'Instantiated image from shape {}'.format(shape)
        if name:
            event = '{} as {}'.format(event, name)
        if log_in_history:
            self.history.append(event)
        
    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.name = getattr(obj, 'name', None)
        self.history = getattr(obj, 'history', [])

    def png(self, width=None):
        """Return png string of image.

        :param width: integer specifying the desired width
        :returns: png as a string
        """
        skimage.io.use_plugin('freeimage')

        def resize(im, width):
            x, y = im.shape[:2]
            f = float(width) / float(x)
            scale_factors = [1.0 for i in range(len(im.shape))]
            scale_factors[0] = f
            scale_factors[1] = f
            ar = scipy.ndimage.zoom(im, scale_factors, order=0)
            return Image.from_array(ar, log_in_history=False)

        safe_range_im = self

        if self.dtype != np.uint8:
            safe_range_im = 255 * normalise(self)

        if width is not None:
            safe_range_im = resize(safe_range_im, width)

        with TemporaryFilePath(suffix='.png') as tmp:
            skimage.io.imsave(tmp.fpath, safe_range_im.astype(np.uint8), "freeimage")
            with open(tmp.fpath, 'rb') as fh:
                return fh.read()

    def _repr_png_(self):
        """Return image as png string.

        Used by IPython qtconsole/notebook to display images.
        """
        return self.png()

class ProxyImage(object):
    """Lightweight image class."""

    def __init__(self, fpath, metadata={}):
        self.fpath = fpath
        for key, value in metadata.items():
            self.__setattr__(key, value)

    def __repr__(self):
        return "<ProxyImage object at {}>".format(hex(id(self)))

    def __info_html_table__(self, index):
        return "<table><tr><th>Index</th><td>{}</td></tr></table>".format(index)

    @property
    def image(self):
        """Underlying :class:`jicbioimage.core.image.Image` instance."""
        return Image.from_file(self.fpath)

    def _repr_png_(self):
        """Return image as png string.

        Used by IPython qtconsole/notebook to display images.
        """
        return self.image.png()

class MicroscopyImage(ProxyImage):
    """Lightweight image class with microscopy meta data."""

    def __repr__(self):
        return "<MicroscopyImage(s={}, c={}, z={}, t={}) object at {}>".format(
            self.series,
            self.channel,
            self.zslice,
            self.timepoint,
            hex(id(self)))

    def __info_html_table__(self, index):
        return """
            <table>
                <tr>
                    <th>Index</th>
                    <th>Series</th>
                    <th>Channel</th>
                    <th>Z-slice</th>
                    <th>Time point</th>
                </tr>
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
            </table>
            """.format(
                index, 
                self.series,
                self.channel,
                self.zslice,
                self.timepoint)

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
        """Return a :class:`jicbioimage.core.image.ProxyImage` instance.
        
        :param index: list index
        :returns: :class:`jicbioimage.core.image.ProxyImage`
        """
        return self[index]

    def image(self, index=0):
        """Return image as a :class:`jicbioimage.core.image.Image`.
        
        :param index: list index
        :returns: :class:`jicbioimage.core.image.Image`
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

    def _repr_html_(self):
        """Return image collection as html.

        Used by IPython notebook to display the image collection.
        """
        DIV_HTML = '''<div style="float: left; padding: 2px;" >{}</div>'''
        CONTENT_HTML = '''<p>{}</p>
            <img style="margin-left: auto; margin-right: auto;"
            src="data:image/png;base64,{}" />
            '''
        
        lines = []
        for i, proxy_image in enumerate(self):
            b64_png = base64.b64encode(proxy_image.image.png(width=300)).decode('utf-8')
            l = DIV_HTML.format(
                    CONTENT_HTML.format(
                        proxy_image.__info_html_table__(i),
                        b64_png
                    )
                )
            lines.append(l)
        return '\n'.join(lines)

class MicroscopyCollection(ImageCollection):
    """Class for storing related :class:`jicbioimage.core.image.MicroscopyImage` instances."""

    def proxy_image(self, s=0, c=0, z=0, t=0):
        """Return a :class:`jicbioimage.core.image.MicroscopyImage` instance.
        
        :param s: series
        :param c: channel
        :param z: zslice
        :param t: timepoint
        :returns: :class:`jicbioimage.core.image.MicroscopyImage`
        """
        for proxy_image in self:
            if proxy_image.is_me(s=s, c=c, z=z, t=t):
                return proxy_image

    def zstack_proxy_iterator(self, s=0, c=0, t=0):
        """Return iterator of :class:`jicbioimage.core.image.ProxyImage` instances in the zstack.
        
        :param s: series
        :param c: channel
        :param t: timepoint
        :returns: zstack :class:`jicbioimage.core.image.ProxyImage` iterator
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
        """Return image as a :class:`jicbioimage.core.image.Image`.
        
        :param s: series
        :param c: channel
        :param z: zslice
        :param t: timepoint
        :returns: :class:`jicbioimage.core.image.Image`
        """
        return self.proxy_image(s=s, c=c, z=z, t=t).image

class DataManager(list):
    """Class for managing :class:`jicbioimage.core.image.ImageCollection` instances."""

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

class SegmentedImage(Image):
    """Class representing the results of applying a segmentation to an image.

    Each unique pixel value represents a different region of the segmentation.
    0 represents background and positive integers represent the different
    regions.
    """

    @property
    def identifiers(self):
        """Return a set of unique identifiers in the segmented image."""

        return set(np.unique(self)) - set([0])

    @property
    def number_of_segments(self):
        """Return the number of segments present in the segmented image."""

        return len(self.identifiers)

    def region_by_identifier(self, identifier):
        """Return region of interest corresponding to the supplied identifier.
       
        :param identifier: integer corresponding to the segment of interest 
        :returns: `jicbioimage.core.region.Region`
        """

        if identifier < 0:
            raise(ValueError("Identifier must be a positive integer."))

        if not np.equal(np.mod(identifier, 1), 0):
            raise(ValueError("Identifier must be a positive integer."))

        if identifier == 0:
            raise(ValueError("0 represents the background."))

        return Region.select_from_array(self, identifier)

    @property
    def background(self):
        """Return the segmented image background.
        
        In other words the region with pixel values 0.

        :returns: `jicbioimage.core.region.Region`
        """

        return Region.select_from_array(self, 0)

    @property
    def false_color_image(self):
        """Return segmentation as a false color image.
        
        :returns: `jicbioimage.core.image.Image`
        """
        return Image.from_array( false_color(self) ) 

    @property
    def grayscale_image(self):
        """Return segmentation using raw identifiers.
        
        :returns: `jicbioimage.core.image.Image`
        """
        return Image.from_array( self ) 

    def png(self, width=None):
        """Return png string of image.

        :param width: integer specifying the desired width
        :returns: png as a string
        """
        return self.false_color_image.png(width) 
