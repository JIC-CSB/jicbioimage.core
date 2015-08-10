Working with microscopy data
============================

One of the main driving forces behind the development of :mod:`jicimagelib` has
been the need to simplify programmatic analysis of microscopy data.

Microscopy data differ from normal images in that they can be multidimensional.
For example a microscopy image can consist of several z-slices, creating
something like a 3D object, as well as several time points, creating something
like a movie.

What this means in practise is that a microscopy datum is in reality a
collection of 2D images. What :mod:`jicimagelib` tries to do is to provide easy
access to the individual 2D images in the microscopy datum. This is achieved by
unzipping the content of the microscopy datum into a backend, which acts as a
type of cache of the individual 2D images.

However, microscopy data comes in a multitude of differing formats and it is
not the intention that :mod:`jicimagelib` should understand these formats
natively. Particularly as this is something that the
`Open Microscopy team <https://www.openmicroscopy.org/site>`_ already
does through its BioFormats project.

In order to be able to process microscopy data :mod:`jicimagelib` therefore
depends on the BioFormats command line tools. In particular the ``bfconvert``
tool, which is used to populate the backend.

For more information on how to install :mod:`jicimagelib` and the BioFormats
command line tools please see the :doc:`installation_notes`.
