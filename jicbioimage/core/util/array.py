"""Module containing utility functions for manipulating numpy arrays."""

import sys
from functools import wraps

import random

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


def false_color(array, color_dict=None, keep_zero_black=True):
    """Return a RGB false color array.

    Assigning a unique RGB color value to each unique element of the input
    array and return an array of shape (array.shape, 3).

    :param array: input numpy.array
    :param color_dict: dictionary with keys/values corresponding to identifiers
                       and RGB tuples respectively
    :param keep_zero_black: whether or not the background should be black
    :returns: numpy.array
    """

    output_array = np.zeros(array.shape + (3,), np.uint8)

    unique_identifiers = set(np.unique(array))

    if color_dict is None:
        color_dict = _pretty_color_palette(
            unique_identifiers, keep_zero_black)

    for identifier in unique_identifiers:
        output_array[np.where(array == identifier)] = color_dict[identifier]

    return output_array


def _pretty_color(identifier=None):
    """Return aesthetically pleasing RGB tuple.

    :returns: RGB tuple
    """
    class Color(dict):
        def swap(self, i, j):
            """Swap two color channels around."""
            tmp = self[i]
            self[i] = self[j]
            self[j] = tmp

        @property
        def rgb_tuple(self):
            """Return RGB tuple."""
            return (self[0].intenisty, self[1].intenisty, self[2].intenisty)

    class Channel(object):
        def __init__(self, seed, start, end, step=1):
            self.seed = seed
            self.choices = range(start, end, step)

        def cut(self, divisor):
            """Return a deck of integers cut at the divisor."""
            split = len(self.choices) // divisor
            start = list(self.choices[split:])
            end = list(self.choices[:split])
            self.choices = start + end

        def reverse(self):
            """Return reversed deck."""
            self.choices = list(reversed(self.choices))

        @property
        def intenisty(self):
            """Return the channel intensity value."""
            pick = self.seed % len(self.choices)
            return self.choices[pick]

    # Create a seed for each channel.
    seed1 = identifier
    if seed1 is None:
        try:
            seed1 = random.randint(0, sys.maxint)
        except AttributeError:
            # Python3 has no sys.maxint
            seed1 = random.randint(0, sys.maxsize)
    seed1 = abs(int(seed1))
    seed2 = seed1 + 30
    seed3 = seed2 ** 2  # Make the seeds non-linear.

    # Create a color object with channels.
    color = Color()
    color[0] = Channel(seed1, 128, 256)
    color[1] = Channel(seed2, 0, 128)
    color[2] = Channel(seed3, 255, 0, -1)

    # Introduce some "randomness" into the first channel
    # using first prime number.
    if seed1 % 2:
        color[0].cut(3)

    # Introduce some "randomness" into one of the channels
    # using second prime number.
    color[seed1 % 3].reverse()

    # Add some more "randomness" using the third prime number.
    order = seed1 % 7
    if order == 0:
        pass
    elif order == 1:
        color.swap(0, 2)
    elif order == 2:
        color.swap(0, 1)
    elif order == 3:
        color.swap(0, 2)
        color.swap(0, 1)
    elif order == 4:
        color.swap(0, 1)
        color.swap(0, 2)
    elif order == 5:
        color.swap(1, 2)
    elif order == 6:
        color[2].cut(2)
        color[2].reverse()

    return color.rgb_tuple


def _pretty_color_palette(identifiers, keep_zero_black=True):
    """Return dictionary with pretty colors.

    :param identifiers: set of unique identifiers
    :param keep_zero_black: whether or not the background should be black
    :returns: dictionary
    """

    color_dict = {}
    for i in identifiers:
        if keep_zero_black and i == 0:
            color_dict[0] = (0, 0, 0)
            continue
        value = _pretty_color(i)
        color_dict[i] = value

    return color_dict
