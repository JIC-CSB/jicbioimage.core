Modules and classes
===================

Classes
-------

:class:`ImageCollectionDataManager` 
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
  **NOT** a subclass of :class:`ImageStack`.

:class:`Channel`
  **NOT** a  subclass of :class:`ImageStack`.

:class:`ZStack`
  A subclass of :class:`ImageStack`.

:class:`TimePoint`
  A subclass of :class:`ImageStack`. **Always of same sample or not.**

:class:`ImageViewer`
  A class for visualising microscopy data. Notably it has the functions
  :func:`ImageViewer.load` and :func:`ImageViewer.add_image_layer`.

:class:`StackViewer`
  A class for visualising microscopy data. Notably it has the functions
  :func:`StackViewer.load`, :func:`StackViewer.add_image_layer` and
  :func:`StackViewer.add_stack_layer`.

:class:`MapTransform`
  Base class for creating classes that transform :class:`Image` and
  :class:`ImageStack` instances using a one-to-one mapping.

:class:`ReduceStack`
  Base class for creating classes that transform :class:`ImageStack` instances
  to :class:`Image` instances.
  
:class:`MapCalculation`
  Base class for creating classes that derive data from :class:`Image` and
  :class:`ImageStack` instances using a one-to-one mapping.

:class:`ReduceCalculation`
  Base class for creating classes that derive data from :class:`Image` and
  :class:`ImageStack` instances to single values.
  
