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
        # And creat args, kwargs stripped of image for history event.
        input_image = kwargs.get("image", None)
        h_args = list(args[:])  # Take a copy and convert to list (in case it is a tuple).
        h_kwargs = kwargs.copy()  # Take a copy.
        if input_image is None:
            input_image = args[0]
            h_args.pop(0)
        else:
            h_kwargs.pop("image")

        # Get the history from the image.
        history = History()
        if hasattr(input_image, "history"):
            history.extend(input_image.history)

        image = func(*args, **kwargs)
        if not isinstance(image, _BaseImageWithHistory):
            image = Image.from_array(image, log_in_history=False)

        # Update the history of the image.
        image.history = history
#       image.history.append('Applied {} transform'.format(func.__name__))
        image.history.add_event(func, h_args, h_kwargs)

        if AutoWrite.on:
            fpath = AutoName.name(func)
            image.write(fpath)
        return image
    return func_as_transformation


class History(list):
    """Class for storing the provenance of an image."""

    class Event(object):
        """An event in the history of an image."""

        def __init__(self, function, args, kwargs):
            self.function = function
            self.args = args
            self.kwargs = kwargs

        def __repr__(self):
            return str(self)

        def __str__(self):
            def quote_strings(value):
                if isinstance(value, str):
                    return "'{}'".format(value)
                return value
            args = [quote_strings(v) for v in self.args]
            kwargs = ["{}={}".format(k, quote_strings(v))
                      for k, v in self.kwargs.iteritems()]
            info = ["image"] + args + kwargs
            info = ", ".join(info)
            return "<History.Event({}({}))>".format(self.function.__name__, info)

        def apply_to(self, image):
            """Apply an event to an image."""
            args = [image,]
            args.extend(self.args)
            return self.function(*args, **self.kwargs)

    def add_event(self, function, args, kwargs):
        """Return event added to the history."""
        event = History.Event(function, args, kwargs)
        self.append(event)
        return event
