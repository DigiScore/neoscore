from brown.utils import units
from brown.config import config
from brown.core import brown
from brown.core.path import Path
from brown.primitives.clef import Clef


class Staff:

    def __init__(self, x, y, length, staff_unit=None, line_count=5):
        self._x = x
        self._y = y
        self._line_count = line_count
        self._length = length
        if staff_unit:
            self.staff_unit = staff_unit * units.mm
        else:
            self.staff_unit = config.DEFAULT_STAFF_UNIT * units.mm
        self._contents = []
        self._grob = Path(self.x, self.y)
        # Draw the staff lines
        for i in range(self.line_count):
            self.grob.move_to(0, i * self.staff_unit)
            self.grob.line_to(self.length, i * self.staff_unit)
        # TODO: More fully implement arbitrary numbers of staff lines

    ######## PUBLIC PROPERTIES ########

    @property
    def grob(self):
        """The core graphical object representation of this StaffObject"""
        return self._grob

    @property
    def x(self):
        """float: x coordinate of the left side of the staff"""
        return self._x

    # @x.setter
    # def x(self, value):
    #     self._x = value

    @property
    def y(self):
        """float: y coordinate of the left side of the staff"""
        return self._y

    # @y.setter
    # def y(self, value):
    #     self._y = value

    @property
    def length(self):
        """float: length coordinate of the left side of the staff"""
        return self._length

    # @length.setter
    # def length(self, value):
    #     self._length = value

    @property
    def height(self):
        """float: The height of the staff in pixels from top to bottom line."""
        # TODO: How should the height of a 1 line staff be defined?
        return (self.line_count - 1) * self.staff_unit

    @property
    def line_count(self):
        """int: The number of lines in the staff"""
        return self._line_count

    @property
    def contents(self):
        """list[StaffObject]: A list of staff objects belonging to the staff"""
        return self._contents

    ######## PRIVATE METHODS ########

    def _register_staff_object(self, staff_object):
        """Add a StaffObject to `self.contents`.

        Args:
            staff_object (StaffObject): The object to add to `self.contents`

        Warning:
            This does not set `staff_object.staff` to self"""
        self._contents.append(staff_object)
        staff_object.staff = self

    ######## PUBLIC METHODS ########

    def active_clef_at(self, position_x):
        """Find and return the active clef at a given point.

        Returns: Clef
        """
        # TODO: Find a more efficient way to quickly look up contents by type
        clefs_before = [item for item in self.contents
                        if isinstance(item, Clef) and
                        item.position_x <= position_x]
        return max(clefs_before, key=lambda c: c.position_x, default=None)

    def middle_c_at(self, position_x):
        """Find the vertical staff position of middle-c at a given point.

        Looks for clefs and other transposing modifiers to determine
        the position of middle-c. If no clef is present, treble is assumed.

        Returns:
            int: A vertical staff position, where 0 means the center
            line or space of the staff, higher numbers mean higher positions,
            and lower numbers mean lower positions.
        """
        clef = self.active_clef_at(position_x)
        if clef is None:
            # Assume treble
            return Clef._middle_c_staff_positions['treble']
        else:
            return clef.middle_c_staff_position

    def _natural_midi_number_of_top_line_at(self, position_x):
        """Find the natural midi pitch class of the top line at a given point.

        Looks for clefs and other transposing modifiers to determine
        the this value. If no clef is present, treble is assumed.

        Returns an `int` midi pitch number.
        """
        clef = self.active_clef_at(position_x)
        if clef is None:
            # Assume treble
            return Clef._natural_midi_numbers_at_top_staff_line['treble']
        else:
            return clef._natural_midi_number_at_top_staff_line

    def render(self):
        """Render the staff.

        Returns: None
        """
        self.grob.render()

    ######## PRIVATE METHODS ########

    def _staff_pos_to_top_down(self, centered_value):
        """Convert a staff position to its top-down equivalent.

        This takes a centered staff position (where 0 means the center
        position positive values mean higher positions, and lower values
        vice versa) and returns its equivalent in the top-down system
        (where 0 means the top line of the staff, negative values
        extend upward, and positive values extend downward).

        This is mostly meant for internal purposes in the rendering
        pipeline. Values should not be stored in objects as these values.

        Args:
            centered_value (int): A staff position in the centered system.

        Returns:
            int: A staff position in the top-down system

        Example:
            # TODO: Make me
        """
        return (-1 * centered_value) + self.line_count - 1

    def _staff_pos_to_rel_pixels(self, centered_value):
        """Convert a staff position to pixels relative to the staff.

        This takes a centered staff position (where 0 means the center
        position positive values mean higher positions, and lower values
        vice versa) and returns its translation to pixels relative to the
        top of the staff, where 0 is the top of the staff, negative values
        extend upward, and positive values extend downward

        Args:
            centered_value (float): A staff position in the centered system.

        Returns:
            float: A y-axis pixel position relative to the top of the staff

        Example:
            # TODO: Make me
        """
        return (self._staff_pos_to_top_down(centered_value) *
                (self.staff_unit / 2))

    def _staff_pos_outside_staff(self, centered_value):
        """bool: Determine if a position is outside of the staff.

        This is true for any position not on or between the outer staff lines.
        """
        return abs(centered_value) > (self.line_count - 1)

    def _position_needs_ledger(self, centered_value):
        """bool: Determine if a position needs a ledger line"""
        # If the position is outside the staff and self.count_count and
        # centered_value's evenness are different, a ledger line is needed
        return (self._staff_pos_outside_staff(centered_value) and
                self.line_count % 2 != centered_value % 2)
