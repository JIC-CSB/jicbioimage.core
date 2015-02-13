Modules and classes
===================

Classes
-------

:class:`ImageDataManager` 
  Contains a list of :class:`ImageCollection` instances.

:class:`ImageCollection`
  Contains attributes and functions for accessing and iterating over
  :class:`Image` and :class:`ImageStack` instances from a microscopy file.

:class:`ImageStack`
  A list of :class:`Image` instances. It would be useful if this class had
  :func:`ImageStack.append` and :func:`ImageStack.extend` functions.

:class:`Image`
  A class inheriting its behaviour from a ``numpy.array`` or possibly
  containing a ``numpy.array`` with the image data.

:class:`Series`
  A subclass of :class:`ImageStack`.

:class:`Channel`
  A subclass of :class:`ImageStack`.

:class:`ZSlice`
  A subclass of :class:`ImageStack`.

:class:`TimePoint`
  A subclass of :class:`ImageStack`.

:class:`ImageViewer`
  A class for visualising microscopy data. Notably it has the functions
  :func:`ImageViewer.load` and :func:`ImageViewer.add_layer`.

:class:`MapTransform`
  Base class for creating classes that transform :class:`Image` and
  :class:`ImageStack` instances using a one-to-one mapping.

:class:`ReduceTransform`
  Base class for creating classes that transform :class:`ImageStack` instances
  to :class:`Image` instances.
  
:class:`MapCalculation`
  Base class for creating classes that derive data from :class:`Image` and
  :class:`ImageStack` instances using a one-to-one mapping.

:class:`ReduceCalculation`
  Base class for creating classes that derive data from :class:`Image` and
  :class:`ImageStack` instances to single values.
  
