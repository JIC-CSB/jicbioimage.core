"""Module containing utility functions for manipulating numpy arrays."""

import sys
from functools import wraps

import random

import numpy as np

from jicbioimage.core.util.color import pretty_color_palette, unique_color_palette

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


def reduce_stack(array3D, z_function):
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


def map_stack(array3D, z_function):
    """Return 3D array where each z-slice has had the function applied to it.

    :param array3D: 3D numpy.array
    :param z_function: function to be mapped to each z-slice
    """
    _, _, zdim = array3D.shape
    return np.dstack([z_function(array3D[:, :, z]) for z in range(zdim)])


def check_dtype(array, allowed):
    """Raises TypeError if the array is not of an allowed dtype.

    :param array: array whose dtype is to be checked
    :param allowed: instance or list of allowed dtypes
    :raises: TypeError
    """
    if not hasattr(allowed, "__iter__"):
        allowed = [allowed, ]
    if array.dtype not in allowed:
        msg = "Invalid dtype {}. Allowed dtype(s): {}"
        raise(TypeError(msg.format(array.dtype, allowed)))


def dtype_contract(input_dtype=None, output_dtype=None):
    """Function decorator for specifying input and/or output array dtypes.

    :param input_dtype: dtype of input array
    :param output_dtype: dtype of output array
    :returns: function decorator
    """
    def wrap(function):
        @wraps(function)
        def wrapped_function(*args, **kwargs):
            if input_dtype is not None:
                check_dtype(args[0], input_dtype)
            array = function(*args, **kwargs)
            if output_dtype is not None:
                check_dtype(array, output_dtype)
            return array
        return wrapped_function
    return wrap


def color_array(array, color_dict):
    """Return RGB color array.

    Assigning a unique RGB color value to each unique element of the input
    array and return an array of shape (array.shape, 3).

    :param array: input numpy.array
    :param color_dict: dictionary with keys/values corresponding to identifiers
                       and RGB tuples respectively
    """
    output_array = np.zeros(array.shape + (3,), np.uint8)
    unique_identifiers = set(np.unique(array))
    for identifier in unique_identifiers:
        output_array[np.where(array == identifier)] = color_dict[identifier]
    return output_array


def pretty_color_array(array, keep_zero_black=True):
    """Return a RGB pretty color array.

    Assigning a pretty RGB color value to each unique element of the input
    array and return an array of shape (array.shape, 3).

    :param array: input numpy.array
    :param keep_zero_black: whether or not the background should be black
    :returns: numpy.array
    """
    unique_identifiers = set(np.unique(array))
    color_dict = pretty_color_palette(unique_identifiers, keep_zero_black)
    return color_array(array, color_dict)


def unique_color_array(array):
    """Return a RGB unique color array.

    Assigning a unique RGB color value to each unique element of the input
    array and return an array of shape (array.shape, 3).

    :param array: input numpy.array
    :returns: numpy.array
    """
    unique_identifiers = set(np.unique(array))
    color_dict = unique_color_palette(unique_identifiers)
    return color_array(array, color_dict)
