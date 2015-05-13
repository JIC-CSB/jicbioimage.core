"""Module for geometric operations."""

class Point2D(object):
    """Class representing a point in 2D space."""

    def __init__(self, a1, a2=None):
        if a2 is None:
            # We assume that we have given a sequence with x, y coordinates.
            self.x, self.y = a1
        else:
            self.x = a1
            self.y = a2

    def __repr__(self):
        if isinstance(self.x, float) or isinstance(self.y, float):
            return "<Point2D(x={:.2f}, y={:.2f})>".format(self.x, self.y)
        return "<Point2D(x={}, y={})>".format(self.x, self.y)
