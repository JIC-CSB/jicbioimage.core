"""Module for storing transformation functions."""

import numpy as np
import PIL.Image

from jicimagelib.io import AutoName, AutoWrite
from jicimagelib.image import Image
from jicimagelib.util.array import normalise, project_by_function

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
    return project_by_function(stack, max)

@transformation
def min_intensity_projection(stack):
    """Return minimum intensity projection of a stack.
    
    :param stack: 3D array from which to project third dimension 
    :returns: :class:`jicimagelib.image.Image`
    """
    return project_by_function(stack, min)
