"""Module for storing transformation functions."""

from jicimagelib.io import AutoName, AutoWrite
import PIL.Image
def transformation(func):
    """Function decorator to turn another function into a transformation."""
    def func_as_transformation(*args, **kwargs):
        image = func(*args, **kwargs)
        image.history.append('Applied {} transform'.format(func.__name__))
        if AutoWrite.on:
            fpath = AutoName.name(func)
            pil_im = PIL.Image.fromarray(args[0])
            pil_im.save(fpath)
        return image
    return func_as_transformation
    
    return func

