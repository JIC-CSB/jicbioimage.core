"""Module for managing and accessing images."""

import os
import json
import base64
import tempfile

import numpy as np
import scipy.ndimage
import skimage.io

from jicbioimage.core.util.array import normalise


class _TemporaryFilePath(object):
    """Temporary file path context manager."""
    def __init__(self, suffix):
        self.suffix = suffix

    def __enter__(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix=self.suffix,
                                               delete=False)
        self.fpath = tmp_file.name
        tmp_file.close()
        return self

    def __exit__(self, type, value, tb):
        os.unlink(self.fpath)


class _BaseImage(np.ndarray):
    """Private image base class with png repr functionality.

    Needed to split out the png functionality from the
    :class:`jicbioimage.core.image.Image` class in order to be able to re-use
    it in :class:`jicbioimage.illustrate.Canvas`.

    This base class will remain private until we can find a suitable name for
    it.
    """

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

        with _TemporaryFilePath(suffix='.png') as tmp:
            safe_range_im_uint8 = safe_range_im.astype(np.uint8)
            skimage.io.imsave(tmp.fpath, safe_range_im_uint8, "freeimage")
            with open(tmp.fpath, 'rb') as fh:
                return fh.read()

    def _repr_png_(self):
        """Return image as png string.

        Used by IPython qtconsole/notebook to display images.
        """
        return self.png()


class Image(_BaseImage):
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


class ProxyImage(object):
    """Lightweight image class."""

    def __init__(self, fpath, metadata={}):
        self.fpath = fpath
        for key, value in metadata.items():
            self.__setattr__(key, value)

    def __repr__(self):
        return "<ProxyImage object at {}>".format(hex(id(self)))

    def __info_html_table__(self, index):
        table = "<table><tr><th>Index</th><td>{}</td></tr></table>"
        return table.format(index)

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
            """.format(index,
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

    def __init__(self, fpath=None):
        if fpath is not None:
            self.parse_manifest(fpath)

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
        :raises: RuntimeError
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
            png = proxy_image.image.png(width=300)
            b64_png = base64.b64encode(png).decode('utf-8')
            l = DIV_HTML.format(
                CONTENT_HTML.format(
                    proxy_image.__info_html_table__(i),
                    b64_png
                )
            )
            lines.append(l)
        return '\n'.join(lines)


class MicroscopyCollection(ImageCollection):
    """
    Collection of :class:`jicbioimage.core.image.MicroscopyImage` instances.
    """

    @property
    def series(self):
        """Return list of series in the collection."""
        return sorted(list(set([mi.series for mi in self])))

    def channels(self, s=0):
        """Return list of channels in the collection.

        :param s: series
        :returns: list of channel identifiers
        """
        return sorted(list(set([mi.channel for mi in self if mi.series == s])))

    def zslices(self, s=0):
        """Return list of z-slices in the collection.

        :param s: series
        :returns: list of zslice identifiers
        """
        return sorted(list(set([mi.zslice for mi in self if mi.series == s])))

    def timepoints(self, s=0):
        """Return list of time points in the collection.

        :param s: series
        :returns: list of time point identifiers
        """
        return sorted(list(set([mi.timepoint for mi in self
                                if mi.series == s])))

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
        """
        Return zstack :class:`jicbioimage.core.image.ProxyImage` iterator.

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
        zstack = [x.image for x in self.zstack_proxy_iterator(s=s, c=c, t=t)]
        return np.dstack(zstack)

    def image(self, s=0, c=0, z=0, t=0):
        """Return image as a :class:`jicbioimage.core.image.Image`.

        :param s: series
        :param c: channel
        :param z: zslice
        :param t: timepoint
        :returns: :class:`jicbioimage.core.image.Image`
        """
        return self.proxy_image(s=s, c=c, z=z, t=t).image
