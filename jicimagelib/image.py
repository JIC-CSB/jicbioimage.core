"""Module for managing and accessing images."""

class ImageProxy(object):
    """Image class."""

    def __init__(self, fpath):
        self.fpath = fpath

class ImageCollection(list):
    """Class for storing related images."""

    def add_image_proxy(self, image_proxy):
        """Add an :class:`jicimagelib.image.ImageProxy` to the collection."""
        self.append(image_proxy)


class DataManager(list):
    """Class for managing :class:`ImageCollection` instances."""

    def load(self, fpath):
        """Load a microscopy file."""
        image_collection = ImageCollection()
        image_proxy = ImageProxy(fpath)
        image_collection.add_image_proxy(image_proxy)
        self.append(image_collection)

