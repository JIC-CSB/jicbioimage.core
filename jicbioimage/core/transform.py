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

import skimage.io
import skimage.morphology
import skimage.exposure

from jicbioimage.core.io import AutoName, AutoWrite
from jicbioimage.core.image import Image
from jicbioimage.core.util.array import normalise


def transformation(func):
    """Function decorator to turn another function into a transformation."""
    @wraps(func)
    def func_as_transformation(*args, **kwargs):
        image = func(*args, **kwargs)
        if not isinstance(image, Image):
            image = Image.from_array(image, log_in_history=False)

        image.history.append('Applied {} transform'.format(func.__name__))

        if AutoWrite.on:
            fpath = AutoName.name(func)
            with open(fpath, "wb") as fh:
                fh.write(image.png())
        return image
    return func_as_transformation
