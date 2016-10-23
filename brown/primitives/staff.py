from brown.utils import units
from brown.config import config
from brown.core import brown
from brown.core.path import Path


# mock up staff


class Staff:

    def __init__(self, x, y, length, staff_unit=None):
        self._x = x
        self._y = y
        self.line_count = 5
        self._length = length
        if staff_unit:
            self.staff_unit = staff_unit * units.mm
        else:
            self.staff_unit = config.DEFAULT_STAFF_UNIT * units.mm
        self.contents = []
        self.grob = Path(self.x, self.y)
        # Draw the staff lines
        for i in range(self.line_count):
            self.grob.move_to(0, i * self.staff_unit)
            self.grob.line_to(self.length, i * self.staff_unit)

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
    def length(self):
        """float: length coordinate of the left side of the staff"""
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def height(self):
        """float: The height of the staff in pixels, from top to bottom line."""
        return (self.line_count - 1) * self.staff_unit

    ######## Public Methods ########

    # def center_position_at(self, position_x):
    #     """Find the (natural) pitch corresponding to the middle
    #     staff line or space at a given x position.

    #     Looks for clefs and other transposing modifiers.
    #     If no clef is present, treble is assumed.

    #     Returns a
    #     """


    def middle_c_at(self, position_x):
        """Find the vertical staff position of middle-c at a given point.

        Looks for clefs and other transposing modifiers to determine
        the position of middle-c. If no clef is present, treble is assumed.

        Returns an `int` vertical staff position, where 0 means the center
        line or space of the staff, higher numbers mean higher pitches,
        and lower numbers mean lower pitches.
        """
        # TODO: Revisit once clefs and other transposition modifiers
        #       are implemented.
        #       assumes for now that everything is treble clef.
        return -6

    def natural_midi_number_of_top_line_at(self, position_x):
        """Find the natural midi pitch class of the top line at a given point.

        Looks for clefs and other transposing modifiers to determine
        the this value. If no clef is present, treble is assumed.

        Returns an `int` midi pitch number.
        """
        # TODO: This currently assumes treble clef
        return 77




    def render(self):
        """Render the staff.

        Returns: None
        """
        self.grob.render()
