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

"""

from functools import wraps

from jicbioimage.core.io import AutoName, AutoWrite
from jicbioimage.core.image import Image, _BaseImageWithHistory


def transformation(func):
    """Function decorator to turn another function into a transformation."""
    @wraps(func)
    def func_as_transformation(*args, **kwargs):

        # Get the input image, so that we can get the history from it.
        input_image = kwargs.get("image", None)
        if input_image is None:
            input_image = args[0]

        # Get the history from the image.
        history = []
        if hasattr(input_image, "history"):
            history.extend(input_image.history)

        image = func(*args, **kwargs)
        if not isinstance(image, _BaseImageWithHistory):
            image = Image.from_array(image, log_in_history=False)

        # Update the history of the image.
        image.history = history
        image.history.append('Applied {} transform'.format(func.__name__))

        if AutoWrite.on:
            fpath = AutoName.name(func)
            image.write(fpath)
        return image
    return func_as_transformation
