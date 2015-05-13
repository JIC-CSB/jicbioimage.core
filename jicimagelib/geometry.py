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

        self._set_types()

    def _set_types(self):
        """Make sure that x, y have consistent types and set dtype."""
        # If we given something that is not an int or a float we raise
        # a RuntimeError as we do not want to have to guess if the given
        # input should be interpreted as an int or a float, for example the
        # interpretation of the string "1" vs the interpretation of the string
        # "1.0".
        for c in (self.x, self.y):
            if not ( isinstance(c, int) or isinstance(c, float) ):
                raise(RuntimeError('x, y coords should be int or float'))

        if isinstance(self.x, int) and isinstance(self.y, int):
            self._dtype = "int"
        else:
            # At least one value is a float so promote both to float.
            self.x = float(self.x)
            self.y = float(self.y)
            self._dtype = "float"

    @property
    def dtype(self):
        """Return the type of the x, y coordinates as a string."""
        return self._dtype

    def __repr__(self):
        s = "<Point2D(x={}, y={}, dtype={})>"
        if self.dtype == "float":
            s = "<Point2D(x={:.2f}, y={:.2f}, dtype={})>"
        return s.format( self.x, self.y, self.dtype)

    def __eq__(self, other):
        if self.dtype != other.dtype:
            return False 
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point2D( self.x + other.x, self.y + other.y ) 

    def __sub__(self, other):
        return Point2D( self.x - other.x, self.y - other.y ) 

    def __mul__(self, other):
        return Point2D( self.x * other, self.y * other)
