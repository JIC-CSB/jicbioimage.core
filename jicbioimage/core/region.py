"""Module for working with regions of interest.

This module contains the :class:`jicbioimage.core.region.Region` class,
which can be used to represent regions of interest.

One can use the
:func:`jicbioimage.core.region.Region.select_from_array` class method
to select a region from a numeric array.

>>> im = np.array([
...     [0, 0, 0, 0, 0, 0, 0],
...     [0, 1, 1, 1, 0, 0, 0],
...     [0, 1, 1, 1, 2, 2, 2],
...     [0, 1, 1, 1, 2, 2, 2],
...     [0, 0, 2, 2, 2, 2, 2],
...     [0, 0, 2, 2, 2, 2, 2],
...     [0, 0, 2, 2, 2, 2, 2]], dtype=np.uint8)
...
>>> Region.select_from_array(im, 2)
Region([[False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False],
       [False, False, False, False,  True,  True,  True],
       [False, False, False, False,  True,  True,  True],
       [False, False,  True,  True,  True,  True,  True],
       [False, False,  True,  True,  True,  True,  True],
       [False, False,  True,  True,  True,  True,  True]], dtype=bool)

Alternatively a region can be created from a bitmap.

>>> import numpy as np
>>> bitmap = np.array([
...     [False, False, False, False, False, False, False],
...     [False,  True, False, False, False,  True, False],
...     [False,  True,  True, False,  True,  True, False],
...     [False,  True,  True,  True,  True,  True, False],
...     [False,  True,  True,  True,  True,  True, False],
...     [False, False,  True,  True,  True, False, False],
...     [False, False, False,  True, False, False, False]], dtype=np.bool)
...
>>> roi = Region(bitmap)

A region has several handy properties.

>>> roi.area
20
>>> roi.perimeter
14

The latter is calculated from the border.

>>> roi.border
Region([[False, False, False, False, False, False, False],
       [False,  True, False, False, False,  True, False],
       [False,  True,  True, False,  True,  True, False],
       [False,  True, False,  True, False,  True, False],
       [False,  True, False, False, False,  True, False],
       [False, False,  True, False,  True, False, False],
       [False, False, False,  True, False, False, False]], dtype=bool)

Another handy property is the convex hull.

>>> roi.convex_hull
Region([[False, False, False, False, False, False, False],
       [False,  True,  True,  True,  True,  True, False],
       [False,  True,  True,  True,  True,  True, False],
       [False,  True,  True,  True,  True,  True, False],
       [False,  True,  True,  True,  True,  True, False],
       [False, False,  True,  True,  True, False, False],
       [False, False, False,  True, False, False, False]], dtype=bool)

"""

import scipy.ndimage as nd
import numpy as np
import skimage
import skimage.morphology

class Region(np.ndarray):
    """Class representing a region of interest in an image.

    The :class:`jicbioimage.core.region.Region` class is a subclass of
    numpy.ndarray.

    However, note that it will compress any data given to it to boolean.

    >>> import numpy as np
    >>> ar = np.array([-1, 0, 1, 2])
    >>> Region(ar)
    Region([ True, False,  True,  True], dtype=bool)

    To select an particular element use the
    :func:`jicbioimage.core.region.Region.select_from_array` class method.

    >>> Region.select_from_array(ar, identifier=2)
    Region([False, False, False,  True], dtype=bool)

    """

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj.astype(bool)

    @classmethod
    def select_from_array(cls, array, identifier):
        """Return a region from a numpy array.
        
        :param array: :class:`numpy.ndarray`
        :param identifier: value representing the region to select in the array
        :returns: :class:`jicbioimage.core.region.Region`
        """

        base_array = np.zeros(array.shape)
        array_coords = np.where(array == identifier)
        base_array[array_coords] = 1

        return cls(base_array)

    @property
    def inner(self):
        """Region formed by taking non-border elements.

        :returns: :class:`jicbioimage.core.region.Region`
        """

        inner_array = nd.morphology.binary_erosion(self)
        return Region(inner_array)

    @property
    def border(self):
        """Region formed by taking border elements.

        :returns: :class:`jicbioimage.core.region.Region`
        """

        border_array = self - self.inner
        return Region(border_array)

    @property
    def convex_hull(self):
        """Region representing the convex hull.

        :returns: :class:`jicbioimage.core.region.Region`
        """
        hull_array = skimage.morphology.convex_hull_image(self)
        return Region(hull_array)

    @property
    def area(self):
        """Number of non-zero elements.

        :returns: int
        """
        return np.count_nonzero(self)

    @property
    def index_arrays(self):
        """All nonzero elements as a pair of arrays."""
        return np.where(self == True)

    @property
    def points(self):
        """Region as a list of points."""
        return list(zip(*self.index_arrays))


    @property
    def perimeter(self):
        """Return the perimiter.

        :returns: int
        """
        return self.border.area

    def dilate(self, iterations=1):
        """Return a dilated region.

        :param iterations: number of iterations to use in dilation
        :returns: :class:`jicbioimage.core.region.Region`
        """
        dilated_array = nd.morphology.binary_dilation(self, 
                                                      iterations=iterations)
        return Region(dilated_array)
