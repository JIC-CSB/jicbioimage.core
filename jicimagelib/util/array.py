"""Module containing utility functions for manipulating numpy arrays."""

import numpy as np

def normalise(array):
    """Return array normalised such that all values are between 0 and 1.

    If all the values in the array are the same the function will return:
    - np.zeros(array.shape, dtype=np.float) if the value is 0 or less
    - np.ones(array.shape, dtype=np.float) if the value is greater than 0

    :param array: numpy.array
    :returns: numpy.array.astype(numpy.float)
    """
    min_val = array.min()
    max_val = array.max()
    array_range = max_val - min_val

    if array_range == 0:
        # min_val == max_val
        if min_val > 0:
            return np.ones(array.shape, dtype=np.float)
        return np.zeros(array.shape, dtype=np.float)

    return (array.astype(np.float) - min_val) / array_range

def project_by_function(array3D, z_function):
    """Return 2D array projection of the input 3D array.

    The input function is applied to each line of an input x, y value.

    :param array3D: 3D numpy.array
    :param z_function: function to use for the projection (e.g. :func:`max`)
    """
    xmax, ymax, _ = array3D.shape
    projection = np.zeros((xmax, ymax), dtype=array3D.dtype)
    for x in range(xmax):
        for y in range(ymax):
            projection[x, y] = z_function(array3D[x, y, :])
    return projection
 
