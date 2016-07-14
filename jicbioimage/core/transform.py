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

import numpy as np

from jicbioimage.core.io import AutoName, AutoWrite
from jicbioimage.core.image import Image, History, _BaseImageWithHistory


def transformation(func):
    """Function decorator to turn another function into a transformation."""
    @wraps(func)
    def func_as_transformation(*args, **kwargs):

        # Take copies of the args and kwargs for use in the history.
        # We will need to remove the image from either the kwargs
        # or the args before we use h_args and h_kwargs to create a
        # history event.
        h_args = list(args[:])
        h_kwargs = kwargs.copy()

        # Get the input image, so that we can get the history from it.
        # Also, strip the image for h_args/h_kwargs.
        input_image = kwargs.get("image", None)
        if input_image is None:
            # The image is the first item of args.
            input_image = args[0]
            h_args.pop(0)
        else:
            # The image is in kwargs.
            h_kwargs.pop("image")

        def array_to_str(value):
            if isinstance(value, np.ndarray):
                value = repr(value)
            return value

        h_args = [array_to_str(v) for v in h_args]
        for key, value in h_kwargs.items():
            h_kwargs[key] = array_to_str(value)

        # Get the history from the image.
        history = History()
        if hasattr(input_image, "history"):
            history.extend(input_image.history)

        image = func(*args, **kwargs)
        if not isinstance(image, _BaseImageWithHistory):
            image = Image.from_array(image, log_in_history=False)

        # Update the history of the image.
        image.history = history
        image.history.add_event(func, h_args, h_kwargs)

        if AutoWrite.on:
            fpath = AutoName.name(func)
            image.write(fpath)
        return image
    return func_as_transformation
