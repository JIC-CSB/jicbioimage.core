"""Module for storing transformation functions."""

import numpy as np
import PIL.Image

import scipy.ndimage.filters

import skimage.morphology

from jicimagelib.io import AutoName, AutoWrite
from jicimagelib.image import Image
from jicimagelib.util.array import (
    normalise,
    reduce_stack,
    dtype_contract,
)

#############################################################################
# Function decorator for creating transforms.
#############################################################################

def transformation(func):
    """Function decorator to turn another function into a transformation."""
    def func_as_transformation(*args, **kwargs):
        
        # When using transforms that return new ndarrays we lose the
        # jicimagelib.image.Image type and the history of the image.
        # One therefore needs to:
        #  - Extract the history from the input jicimagelib.image.Image.
        #  - Apply the transformation, which may return a numpy ndarray.
        #  - Force the image to the jicimagelib.image.Image type.
        #  - Re-attach the extracted history
        if hasattr(args[0], 'history'):
            # Working on jicimagelib.Image.
            history = args[0].history
        else:
            # Working on something without a history, e.g. a ndarray stack.
            history = []
        image = func(*args, **kwargs)
        image = Image.from_array(image)
        image.history = history

        image.history.append('Applied {} transform'.format(func.__name__))
        if AutoWrite.on:
            fpath = AutoName.name(func)
            try:
                if AutoWrite.auto_safe_dtype:
                    safe_range_im = 255 * normalise(image)
                    pil_im = PIL.Image.fromarray(safe_range_im.astype(np.uint8))
                else:
                    pil_im = PIL.Image.fromarray(image)
            except TypeError:
                # Give a more meaningful error message.
                raise(TypeError(
                    "Cannot handle this data type: {}".format(image.dtype)))
            pil_im.save(fpath)
        return image
    return func_as_transformation

#############################################################################
# General purpose transforms.
#############################################################################

@transformation
def max_intensity_projection(stack):
    """Return maximum intensity projection of a stack.
    
    :param stack: 3D array from which to project third dimension 
    :returns: :class:`jicimagelib.image.Image`
    """
    return reduce_stack(stack, max)

@transformation
def min_intensity_projection(stack):
    """Return minimum intensity projection of a stack.
    
    :param stack: 3D array from which to project third dimension 
    :returns: :class:`jicimagelib.image.Image`
    """
    return reduce_stack(stack, min)

@transformation
@dtype_contract(input_dtype=np.float, output_dtype=np.float)
def smooth_gaussian(image, sigma=1):
    """Returns Gaussian smoothed image.

    :param image: numpy array or :class:`jicimagelib.image.Image`
    :param sigma: standard deviation
    :returns: :class:'jicimagelib.image.Image'
    """
    return scipy.ndimage.filters.gaussian_filter(image, sigma=sigma, mode="nearest")

@transformation
@dtype_contract(input_dtype=np.bool, output_dtype=np.bool)
def remove_small_objects(image, min_size=50):
    """Remove small objects from an boolean image.

    :param image: boolean numpy array or :class:`jicimagelib.image.Image`
    :returns: boolean :class:`jicimagelib.image.Image`
    """ 
    return skimage.morphology.remove_small_objects(image, min_size=min_size)
