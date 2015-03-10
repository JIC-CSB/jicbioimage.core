Quick start guide to :mod:`jicimagelib`
=======================================

The :mod:`jicimagelib` package has been designed to make it easy to work with
microscopy images. To illustrate its use we will use
`multi-channel-4D-series.ome.tif
<http://www.openmicroscopy.org/Schemas/Samples/2015-01/bioformats-artificial/multi-channel-4D-series.ome.tif.zip>`_
file.

.. code-block:: python

    >>> fpath = "multi-channel-4D-series.ome.tif"

Let us also define a directory for caching individual files from any microscopy
data that we may load.

.. code-block:: python

    >>> backend_directory = "./backend"


..
    This is just to make the doctest pass.

    >>> import os.path
    >>> import jicimagelib
    >>> JICIMAGLIB = os.path.dirname(jicimagelib.__file__)
    >>> fpath = os.path.join(JICIMAGLIB, "..", "tests", "data", fpath)

Let us set up a :class:`jicimagelib.image.DataManager`. To instantiate a
:class:`jicimagelib.image.DataManager` we need a backend.  Let us make use of a
:class:`jicimagelib.io.FileBackend`.

.. code-block:: python

    >>> from jicimagelib.image import DataManager
    >>> from jicimagelib.io import FileBackend
    >>> backend = FileBackend(backend_directory)
    >>> data_manager = DataManager(backend)

Now let us load the microscopy file into the ``data_manager``.

.. code-block:: python

    >>> data_manager.load(fpath)

The data manager is essentially a list containing
:class:`jicimagelib.image.ImageCollection` instances.

.. code-block:: python

    >>> len(data_manager)
    1
    >>> image_collection = data_manager[0]

And a :class:`jicimagelib.image.ImageCollection` is essentially just a list of
:class:`jicimagelib.image.ImageProxy` instances.

.. code-block:: python

    >>> len(image_collection)
    105
    >>> image_collection  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<jicimagelib.image.ImageProxy object at ...>,
     <jicimagelib.image.ImageProxy object at ...>,
      ...,
     <jicimagelib.image.ImageProxy object at ...>]

..
    Tidy up: remove the ./backend directory we created.

    >>> import shutil
    >>> shutil.rmtree(backend_directory)
