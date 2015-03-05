Modules and classes
===================

Modules
-------

:mod:`jicimagelib.image`
  Contains all classes related to loading and accessing images.

:mod:`jicimagelib.viewer`
  Contains all classes for visualising images and stacks.

:mod:`jicimagelib.transform`
  Contains all classes that transform images into other images.

:mod:`jicimagelib.calculate`
  Contain all classes used to derive data from images.

:mod:`jicimagelib.render`
  Contain all classes used to create draw annotations.

Classes
-------

:class:`jicimagelib.image.DataManager` 
  Contains a list of :class:`ImageCollection` instances and methods for
  accessing the underlying data in convenient ways.

:class:`jicimagelib.image.ImageCollection`
  Contains attributes and functions for accessing and iterating over
  :class:`jicimagelib.image.Image` and :class:`jicimagelib.image.ImageStack` instances
  from a microscopy file.

:class:`jicimagelib.image.ImageStack`
  A class inheriting its behaviour from a ``numpy.ndarray``.  Essentially a 3D
  array with convenience methods for accessing z-slices as if it were a
  list of :class:`jicimagelib.image.Image` instances. It would be useful if this class
  had :func:`jicimagelib.image.ImageStack.append` and
  :func:`jicimagelib.image.ImageStack.extend` functions.

:class:`jicimagelib.image.Image`
  A class inheriting its behaviour from a ``numpy.array`` or possibly
  containing a ``numpy.array`` with the image data.

:class:`jicimagelib.image.Series`
  **NOT** a subclass of :class:`jicimagelib.image.ImageStack`.

:class:`jicimagelib.image.Channel`
  **NOT** a  subclass of :class:`jicimagelib.image.ImageStack`.

:class:`jicimagelib.image.ZStack`
  A subclass of :class:`jicimagelib.image.ImageStack`.

:class:`jicimagelib.image.TimePoint`
  A subclass of :class:`jicimagelib.image.ImageStack`. **Always of same sample or not?**

:class:`jicimagelib.viwer.ImageViewer`
  A class for visualising microscopy data. Notably it has the functions
  :func:`jicimagelib.viwer.ImageViewer.load` and
  :func:`jicimagelib.viwer.ImageViewer.add_image_layer`.

:class:`jicimagelib.viwer.StackViewer`
  A class for visualising microscopy data. Notably it has the functions
  :func:`jicimagelib.viwer.StackViewer.load`,
  :func:`jicimagelib.viwer.StackViewer.add_image_layer` and
  :func:`jicimagelib.viwer.StackViewer.add_stack_layer`.

:class:`jicimagelib.transform.ImageTransform`
  Base class for creating classes that takes a :class:`jicimagelib.image.Image`
  and produces a transformed :class:`jicimagelib.image.Image`.

:class:`jicimagelib.transform.ReduceStack`
  Base class for creating classes that reduce a
  :class:`jicimagelib.image.ImageStack` instance to an
  :class:`jicimagelib.image.Image` instance.
  
:class:`jicimagelib.calculate.ImageCalculation`
  Base class for creating a class that can derive data from a
  :class:`jicimagelib.image.Image` instance.

:class:`jicimagelib.calculate.StackCalculation`
  Base class for creating a class that can derive data from a
  :class:`jicimagelib.image.ImageStack` instance.
