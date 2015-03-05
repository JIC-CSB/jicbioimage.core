Basic usage
===========

To load and work with microscopy data we use a
:class:`jicimagelib.image.DataManager`. This has the advantage that it can load
microscopy files and make them available to the user as augmented ``numpy``
arrays. It also enables "caching" so that any file format conversion only needs
to happen once.

In the simplest instance a :class:`jicimagelib.image.DataManager` makes use of
the BioFormats ``bfconvert`` tool to convert the microscopy file into a series
of tiff files stored in a directory. Note that this is an implementation detail
and the user can seamlessly access the augmented ``numpy`` arrays to work with
data.

In order to store images a :class:`jicimagelib.image.DataManager` requires a
backend. For example a :class:`jicimagelib.image.FileBackend`.

.. code-block:: python

    >>> from jicimagelib.image import FileBackend
    >>> backend = FileBackend('/tmp/jicimagelib')

We can now use the :class:`jicimagelib.image.FileBackend` instance to create a
:class:`jicimagelib.image.DataManager`.

.. code-block:: python

    >>> from jicimagelib.image import DataManager
    >>> data_manager = DataManager(backend)

To load a microscopy file into the :class:`jicimagelib.image.DataManager` we use the
:func:`jicimagelib.image.DataManager.load` function.

.. code-block:: python

    >>> data_manager.load('test1.lif')
    >>> data_manager.load('test2.lif')

.. warning:: If one tries to load a microscopy file with one already opened the
             :class:`ImageCollectionDataManager` will simply re-load the images stored in
             the cache so as to minimise the number of file format conversions
             required. In other words if one has a file in a different directory with
             the same name as a file already loaded the latter would not trigger any
             file format conversion and the data from the first file would be
             re-loaded. For example the command below would not load the new file
             it would load the data stored in the cache from ``test1.lif``.

             .. code-block:: python

                >>> data_manager.load('./different/dir/test1.lif')

The :class:`jicimagelib.image.DataManager` is simply a list that stores
instances of :class:`jicimagelib.image.ImageCollection` instances.

.. code-block:: python

    >>> data_manager.entries
    [<ImageCollection(test1.lif)>, <ImageCollection(test2.lif)>]
    >>> first_entry = data_manager.entries[0]

A :class:`jicimagelib.image.ImageCollection` has several attributes including:

- :attr:`jicimagelib.image.ImageCollection.identifier`
- :attr:`jicimagelib.image.ImageCollection.series`

.. code-block:: python

    >>> first_entry.identifier
    'test1.lif'

.. admonition:: Question

    Should we create a :class:`jicimagelib.image.ImageCollection.Series` class
    that has attributes for channels, z-slices and time points?

The :class:`jicimagelib.image.ImageCollection` class also provides several
functions for accessing the underlying data.

- :func:`jicimagelib.image.ImageCollection.get_image_proxy`
- :func:`jicimagelib.image.ImageCollection.get_image`
- :func:`jicimagelib.image.ImageCollection.get_zstack_iterator`
- :func:`jicimagelib.image.ImageCollection.get_zstack_array`


.. admonition:: Questions

    - Should we rename get_zstack_iterator to get_zstack_proxy_iterator?
    - Should we drop the ``get_`` prefix from these functions?
