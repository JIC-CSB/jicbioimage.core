"""Module containing image transformation functions.

This module contains the function decorator
:func:`jicbioimage.core.transform.transformation` that can be used
to turn functions into image transformations.

Below is an example of how to create a transformation that inverts an image.

>>> import numpy as np
>>> @transformation
... def invert(image):
...     "Return the inverted image."
...     maximum = np.iinfo(image.dtype).max
...     maximum_array = np.ones(image.shape, dtype=image.dtype) * maximum
...     return maximum_array - image
...

The :mod:`jicbioimage.core.transform` module also contains a number of built-in
general purpose transformations that have already had the
:func:`jicbioimage.core.transform.transformation` function decorator applied to
them.
"""

from functools import wraps

import numpy as np

import scipy.ndimage.filters

import skimage.io
import skimage.morphology
import skimage.exposure

from jicbioimage.core.io import AutoName, AutoWrite
from jicbioimage.core.image import Image
from jicbioimage.core.util.array import (
    normalise,
    reduce_stack,
    dtype_contract,
)

#############################################################################
# Function decorator for creating transforms.
#############################################################################

def transformation(func):
    """Function decorator to turn another function into a transformation."""
    @wraps(func)
    def func_as_transformation(*args, **kwargs):
        
        # When using transforms that return new ndarrays we lose the
        # jicbioimage.core.image.Image type and the history of the image.
        # One therefore needs to:
        #  - Extract the history from the input jicbioimage.core.image.Image.
        #  - Apply the transformation, which may return a numpy ndarray.
        #  - Force the image to the jicbioimage.core.image.Image type.
        #  - Re-attach the extracted history
        if hasattr(args[0], 'history'):
            # Working on jicbioimage.core.Image.
            history = args[0].history
        else:
            # Working on something without a history, e.g. a ndarray stack.
            history = []
        image = func(*args, **kwargs)
        image = Image.from_array(image, log_in_history=False)
        image.history = history

        image.history.append('Applied {} transform'.format(func.__name__))
        if AutoWrite.on:
            fpath = AutoName.name(func)
            im_to_save = np.copy(image)
            if AutoWrite.auto_safe_dtype:
                im_to_save = 255 * normalise(im_to_save)
                im_to_save = im_to_save.astype(np.uint8)
            try:
                skimage.io.imsave(fpath, im_to_save, 'freeimage')
            except ValueError:
                # Give a more meaningful error message.
                raise(TypeError(
                    "Cannot handle this data type: {}".format(image.dtype)))
        return image
    return func_as_transformation

#############################################################################
# General purpose transforms.
#############################################################################

@transformation
def max_intensity_projection(stack):
    """Return maximum intensity projection of a stack.
    
    :param stack: 3D array from which to project third dimension 
    :returns: :class:`jicbioimage.core.image.Image`
    """
    return reduce_stack(stack, max)

@transformation
def min_intensity_projection(stack):
    """Return minimum intensity projection of a stack.
    
    :param stack: 3D array from which to project third dimension 
    :returns: :class:`jicbioimage.core.image.Image`
    """
    return reduce_stack(stack, min)

@transformation
@dtype_contract(input_dtype=np.float, output_dtype=np.float)
def smooth_gaussian(image, sigma=1):
    """Returns Gaussian smoothed image.

    :param image: numpy array or :class:`jicbioimage.core.image.Image`
    :param sigma: standard deviation
    :returns: :class:`jicbioimage.core.image.Image`
    """
    return scipy.ndimage.filters.gaussian_filter(image, sigma=sigma, mode="nearest")

@transformation
@dtype_contract(output_dtype=np.float)
def equalize_adaptive_clahe(image, ntiles=8, clip_limit=0.01):
    """Return contrast limited adaptive histogram equalized image.
    
    The return value is normalised to the range 0 to 1.

    :param image: numpy array or :class:`jicbioimage.core.image.Image` of dtype float
    :param ntiles: number of tile regions
    :param clip_limit: clipping limit in range 0 to 1,
                       higher values give more contrast
    """
    # Convert input for skimage.
    skimage_float_im = normalise(image)
    
    if np.all(skimage_float_im):
        raise(RuntimeError("Cannot equalise when there is no variation."))
    
    normalised = skimage.exposure.equalize_adapthist(skimage_float_im,
        ntiles_x=ntiles, ntiles_y=ntiles, clip_limit=clip_limit)

    assert np.max(normalised) == 1.0
    assert np.min(normalised) == 0.0

    return normalised

@transformation
@dtype_contract(output_dtype=np.bool)
def threshold_otsu(image, multiplier=1.0):
    """Return image thresholded using Otsu's method.
    """
    otsu_value = skimage.filters.threshold_otsu(image)
    return image > otsu_value * multiplier

@transformation
@dtype_contract(input_dtype=np.bool, output_dtype=np.bool)
def remove_small_objects(image, min_size=50):
    """Remove small objects from an boolean image.

    :param image: boolean numpy array or :class:`jicbioimage.core.image.Image`
    :returns: boolean :class:`jicbioimage.core.image.Image`
    """ 
    return skimage.morphology.remove_small_objects(image, min_size=min_size)