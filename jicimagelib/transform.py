"""Module for storing transformation functions."""

from jicimagelib.io import AutoName, AutoWrite
from jicimagelib.image import Image

import PIL.Image

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
                pil_im = PIL.Image.fromarray(image)
            except TypeError:
                # Give a more meaningful error message.
                raise(TypeError(
                    "Cannot handle this data type: {}".format(image.dtype)))
            pil_im.save(fpath)
        return image
    return func_as_transformation
