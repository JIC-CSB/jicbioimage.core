"""Module for working with regions of interest.

This module contains the :class:`jicimagelib.region.Region` class,
which can be used to represent regions of interest.

One can use the
:func:`jicimagelib.region.Region.select_from_array` class method
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
array([[False, False, False, False, False, False, False],
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
array([[False, False, False, False, False, False, False],
       [False,  True, False, False, False,  True, False],
       [False,  True,  True, False,  True,  True, False],
       [False,  True, False,  True, False,  True, False],
       [False,  True, False, False, False,  True, False],
       [False, False,  True, False,  True, False, False],
       [False, False, False,  True, False, False, False]], dtype=bool)

Another handy property is the convex hull.

>>> roi.convex_hull
array([[False, False, False, False, False, False, False],
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

class Region(object):
    """Class representing a region of interest in an image.

    Represented as a bitmask with True indicating the region of interest.
    """

    def __init__(self, bitmap):
        bitmap_values = set(np.unique(bitmap))
        if len(bitmap_values - set([0, 1])):
            raise(ValueError('Region bitmap must have only 0 and 1 values'))

        self.bitmap = bitmap.astype(bool)

    @classmethod
    def select_from_array(cls, array, identifier):
        """Return a region from a numpy array.
        
        :param array: :class:`numpy.ndarray`
        :param identifier: value representing the region to select in the array
        :returns: :class:`jicimagelib.region.Region`
        """

        base_array = np.zeros(array.shape)
        array_coords = np.where(array == identifier)
        base_array[array_coords] = 1

        return cls(base_array)

    @property
    def inner(self):
        """Region formed by taking non-border elements.

        :returns: :class:`jicimagelib.region.Region`
        """

        inner_array = nd.morphology.binary_erosion(self.bitmap)
        return Region(inner_array)

    @property
    def border(self):
        """Region formed by taking border elements.

        :returns: :class:`jicimagelib.region.Region`
        """

        border_array = self.bitmap - self.inner.bitmap
        return Region(border_array)

    @property
    def convex_hull(self):
        """Region representing the convex hull.

        :returns: :class:`jicimagelib.region.Region`
        """
        hull_array = skimage.morphology.convex_hull_image(self.bitmap)
        return Region(hull_array)

    @property
    def area(self):
        """Number of non-zero elements.

        :returns: int
        """
        return np.count_nonzero(self.bitmap)

    @property
    def index_arrays(self):
        """All nonzero elements as a pair of arrays."""
        return np.where(self.bitmap == True)

    @property
    def points(self):
        """Region as a list of points."""
        return zip(*self.index_arrays)


    @property
    def perimeter(self):
        """Return the perimiter.

        :returns: int
        """
        return self.border.area

    def dilate(self, iterations=1):
        """Return a dilated region.

        :param iterations: number of iterations to use in dilation
        :returns: :class:`jicimagelib.region.Region`
        """
        dilated_array = nd.morphology.binary_dilation(self.bitmap, 
                                                      iterations=iterations)
        return Region(dilated_array)

    def __repr__(self):
        return self.bitmap.__repr__()

    def __str__(self):
        return self.bitmap.__str__()
