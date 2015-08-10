Image collections
=================

Introduction
------------

There are two image collection classes:

- :class:`jicimagelib.image.ImageCollection`
- :class:`jicimagelib.image.MicroscopyCollection`

These are used for managing access to the :class:`jicimagelib.image.Image`,
:class:`jicimagelib.image.ProxyImage` and
:class:`jicimagelib.image.MicroscopyImage` stored within them.

The :func:`jicimagelib.image.ImageCollection.image` and
:func:`jicimagelib.image.ImageCollection.proxy_image` functions simply take an
``index`` as an argument and return the relevant item from the collection.

However, the accessor fuctions on the
:class:`jicimagelib.image.MicroscopyCollection` are more advanced in that they
can take arguments for specifying the series, channel, zslice and timepoint of
interest. For more information have a look at the API documentation of:

- :func:`jicimagelib.image.MicroscopyCollection.image`
- :func:`jicimagelib.image.MicroscopyCollection.proxy_image`
- :func:`jicimagelib.image.MicroscopyCollection.zstack_proxy_iterator`
- :func:`jicimagelib.image.MicroscopyCollection.zstack_array`


Obtaining image collections
---------------------------

One can obtain a basic :class:`jicimagelib.image.ImageCollection` by loading a
multipage TIFF file into a :class:`jicimagelib.image.DataManager`.  Let us
therefore create a :class:`jicimagelib.image.DataManager`.

.. code-block:: python

    >>> backend_directory = "./backend"
    >>> from jicimagelib.image import DataManager
    >>> from jicimagelib.io import FileBackend
    >>> backend = FileBackend(backend_directory)
    >>> data_manager = DataManager(backend)

Into which we can load the sample ``multipage.tif`` file.

.. code-block:: python

    >>> multipagetiff_fpath = "./tests/data/multipage.tif"

..
    This is just to make the doctest pass.

    >>> import os.path
    >>> multipagetiff_fpath = os.path.basename(multipagetiff_fpath)
    >>> import os.path
    >>> import jicimagelib
    >>> JICIMAGLIB = os.path.dirname(jicimagelib.__file__)
    >>> multipagetiff_fpath = os.path.join(JICIMAGLIB, "..", "tests", "data", multipagetiff_fpath)

The :func:`jicimagelib.image.DataManager.load` function returns the image
collection.

.. code-block:: python

    >>> image_collection = data_manager.load(multipagetiff_fpath)
    >>> type(image_collection)
    <class 'jicimagelib.image.ImageCollection'>
    
Which contains a number of :class:`jicimagelib.image.ProxyImage` instances.

.. code-block:: python

    >>> image_collection  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<ProxyImage object at ...>,
     <ProxyImage object at ...>,
     <ProxyImage object at ...>]


.. _accessing-data-from-microscopy-collections:

Accessing data from microscopy collections
------------------------------------------

Suppose instead that we had a microscopy file. Here we will use the 
`z-series.ome.tif
<http://www.openmicroscopy.org/Schemas/Samples/2015-01/bioformats-artificial/z-series.ome.tif.zip>`_
file.

.. code-block:: python

    >>> zseries_fpath = "z-series.ome.tif"

..
    This is just to make the doctest pass.

    >>> zseries_fpath = os.path.join(JICIMAGLIB, "..", "tests", "data", zseries_fpath)


Let us now load a microscopy file instead.

.. code-block:: python

    >>> microscopy_collection = data_manager.load(zseries_fpath)
    >>> type(microscopy_collection)
    <class 'jicimagelib.image.MicroscopyCollection'>
    >>> microscopy_collection  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<MicroscopyImage(s=0, c=0, z=0, t=0) object at ...>,
     <MicroscopyImage(s=0, c=0, z=1, t=0) object at ...>,
     <MicroscopyImage(s=0, c=0, z=2, t=0) object at ...>,
     <MicroscopyImage(s=0, c=0, z=3, t=0) object at ...>,
     <MicroscopyImage(s=0, c=0, z=4, t=0) object at ...>]


One can now use a variety of methods to access the underlying microscopy
images. For example to access the third z-slice one could use the code snipped
below.

.. code-block:: python

    >>> microscopy_collection.proxy_image(z=2)  # doctest: +ELLIPSIS
    <MicroscopyImage(s=0, c=0, z=2, t=0) object at ...>

Alternatively to access the raw underlying image data of the same z-slice one
could use the code snippet below.

.. code-block:: python

    >>> microscopy_collection.image(z=2)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Image([[ 0,  0,  0, ...,  0,  0,  0],
           [ 1,  1,  1, ...,  1,  1,  1],
           [ 2,  2,  2, ...,  2,  2,  2],
           ..., 
           [95, 95, 95, ..., 95, 95, 95],
           [95, 95, 95, ..., 95, 95, 95],
           [96, 96, 96, ..., 96, 96, 96]], dtype=uint8)

Similarly one could loop over all the slices in the z-stack using the code
snippet below.

.. code-block:: python

    >>> for i in microscopy_collection.zstack_proxy_iterator():  # doctest: +ELLIPSIS
    ...     print(i)
    ...
    <MicroscopyImage(s=0, c=0, z=0, t=0)>
    <MicroscopyImage(s=0, c=0, z=1, t=0)>
    <MicroscopyImage(s=0, c=0, z=2, t=0)>
    <MicroscopyImage(s=0, c=0, z=3, t=0)>
    <MicroscopyImage(s=0, c=0, z=4, t=0)>


Finally, one can also access the z-stack as a :class:`numpy.ndarray`.

.. code-block:: python

    >>> microscopy_collection.zstack_array()  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    array([[[ 0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0],
            ...
            [96, 96, 96, 96, 96],
            [96, 96, 96, 96, 96],
            [96, 96, 96, 96, 96]]], dtype=uint8)
    


..
    Tidy up: remove the ./backend directory we created.

    >>> import shutil
    >>> shutil.rmtree(backend_directory)
