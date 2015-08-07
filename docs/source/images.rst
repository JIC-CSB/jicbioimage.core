Images
======

Introduction
------------

There are several types of images in the :mod:`jicimagelib.image` module. The
raw data is contained in :class:`jicimagelib.image.Image` class whereas the
:class:`jicimagelib.image.ProxyImage` and
:class:`jicimagelib.image.MicroscopyImage` simply contain a reference to the
raw image along with meta data about the image.

The :class:`jicimagelib.image.Image` is a subclass of :class:`numpy.ndarray`.
In addition to the :class:`numpy.ndarray` functionality the
:class:`jicimagelib.image.Image` class has specialised functionality for
creating images, tracking the history of images and returning png/html
representations of images.

The :class:`jicimagelib.image.MicroscopyImage` class is a subclass of the
:class:`jicimagelib.image.ProxyImage` class. It contains the specialised
functions :func:`jicimagelib.image.MicroscopyImage.is_me` and
:func:`jicimagelib.image.MicroscopyImage.in_zstack`. These functions are used
by the accessor functions in the
:class:`jicimagelib.image.MicroscopyCollection`, for more information please
see :ref:`accessing-data-from-microscopy-collections`.


Creating images
---------------

Using :mod:`numpy` to create images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several ways of creating images. One can use the
functionality inherited from :class:`numpy.ndarray`.

.. code-block:: python

    >>> from jicimagelib.image import Image
    >>> Image((50,50))  # doctest: +SKIP
    Image([[  0,   0,   0, ..., 132,   0,   0],
           [ 90,  57,   0, ..., 101,  62,   0],
           [ 60, 100,  32, ...,   0, 100,  35],
           ...,
           [  0,   0, 208, ...,   0,   0,   0],
           [128,  68,  30, ...,   0, 128, 228],
           [ 34,   1,   1, ...,  69,  30,   2]], dtype=uint8)

.. warning:: When creating an image in this fashion it will be filled with
             the noise of whatever was present in that piece of computer memory
             before the memory was allocated to the image.

A safer way to create an image is to first create a :class:`numpy.ndarray`
using :func:`numpy.zeros` or :func:`numpy.ones` and then cast it to the
:class:`jicimagelib.image.Image` type.

.. code-block:: python

    >>> import numpy as np
    >>> np.zeros((50,50), dtype=np.uint8).view(Image)
    Image([[0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           ..., 
           [0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0]], dtype=uint8)

When creating an array in this fashion it's history is empty.

.. code-block:: python

    >>> np.zeros((50,50), dtype=np.uint8).view(Image).history
    []

To assign a creation event to the image history one can use the
:func:`jicimagelib.image.Image.from_array` class method.

.. code-block:: python

    >>> ar = np.zeros((50,50), dtype=np.uint8)
    >>> im = Image.from_array(ar)
    >>> im.history
    ['Created image from array']

Creating images from file
^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose that we wanted to create an :class:`jicimagelib.image.Image` instance
from the file ``tjelvar.png``.

.. code-block:: python

    >>> fpath = "tjelvar.png"

..
    This is just to make the doctest pass.

    >>> import os.path
    >>> import jicimagelib
    >>> JICIMAGLIB = os.path.dirname(jicimagelib.__file__)
    >>> fpath = os.path.join(JICIMAGLIB, "..", "tests", "data", fpath)

This can be achieved using the :func:`jicimagelib.image.Image.from_file` class
method.

.. code-block:: python

    >>> Image.from_file(fpath)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Image([[[ 97,  86,  85],
            [102,  91,  88],
            [106,  97,  95],
            ...,
            [ 16,   5,  21],
            [ 19,   7,  23],
            [ 15,   5,  21]]], dtype=uint8)


.. TODO:: Document png and _repr_png_ functions.
