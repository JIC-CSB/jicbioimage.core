import scipy.ndimage as nd
import numpy as np
import skimage
import skimage.morphology

class Region(object):
    """Class representing a particular point of interest in an image, 
    represented as a bitmask with 1 indicating areas in the region."""

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
        """Region formed by taking non-border elements."""

        inner_array = nd.morphology.binary_erosion(self.bitmap)
        return Region(inner_array)

    @property
    def border(self):
        """Region formed by taking border elements."""

        border_array = self.bitmap - self.inner.bitmap
        return Region(border_array)

    @property
    def convex_hull(self):
        """Return region representing the convex hull."""
        hull_array = skimage.morphology.convex_hull_image(self.bitmap)
        return Region(hull_array)

    @property
    def area(self):
        """Number of non-zero elements."""
        return np.count_nonzero(self.bitmap)

    @property
    def index_arrays(self):
        """All nonzero elements as a pair of arrays."""
        return np.where(self.bitmap == True)

    @property
    def points(self):
        """Return a list of points."""
        return zip(*self.index_arrays)


    @property
    def perimeter(self):
        """Return the perimiter."""
        return self.border.area

    def dilate(self, iterations=1):
        """Return a dilated region."""
        dilated_array = nd.morphology.binary_dilation(self.bitmap, 
                                                      iterations=iterations)
        return Region(dilated_array)

    def __repr__(self):
        return self.bitmap.__repr__()

    def __str__(self):
        return self.bitmap.__str__()
