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
