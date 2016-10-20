from brown.utils import units
from brown.config import config
from brown.core import brown
from brown.core.path import Path


# mock up stuff


class Staff:

    def __init__(self, x, y, length, height=None):
        self._x = x
        self._y = y
        self._length = length
        if height:
            self._height = height
        else:
            self._height = config.DEFAULT_STAFF_HEIGHT * units.mm
        self.contents = []
        self.grob = Path(self.x, self.y)
        # Draw the staff lines
        line_distance = self.height / 5
        for i in range(5):
            self.grob.move_to(0,
                              i * line_distance)
            self.grob.line_to(self.length,
                              i * line_distance)


    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """float: x coordinate of the left side of the staff"""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """float: y coordinate of the left side of the staff"""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def height(self):
        """float: height coordinate of the left side of the staff"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def length(self):
        """float: length coordinate of the left side of the staff"""
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    ######## Public Methods ########

    def render(self):
        """Render the staff.

        Returns: None
        """
        self.grob.render()
