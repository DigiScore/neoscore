from brown.utils.units import GraphicUnit
from brown.utils.point import Point
from brown.config import config
from brown.core.path import Path
from brown.primitives.clef import Clef



class Staff:
    """A staff capable of holding `StaffObject`s"""

    def __init__(self, pos, length, staff_unit=None, line_count=5):
        """
        Args:
            pos (Point): The position of the top-left corner of the staff
            length (Unit): The horizontal length of the staff
            staff_unit (Unit): The distance between two lines in the staff.
                If not set, this will default to config.DEFAULT_STAFF_UNIT
            line_count (int): The number of lines in the staff.
        """
        self._pos = Point(pos)
        self._x = self._pos.x
        self._y = self._pos.x
        self._line_count = line_count
        self._length = length
        if staff_unit:
            self.staff_unit = staff_unit
        else:
            self.staff_unit = config.DEFAULT_STAFF_UNIT
        self._contents = []
        self._grob = Path(self.pos)
        # Draw the staff lines
        for i in range(self.line_count):
            self.grob.move_to((GraphicUnit(0), self.staff_unit * i))
            self.grob.line_to((self.length, self.staff_unit * i))

    ######## PUBLIC PROPERTIES ########

    @property
    def grob(self):
        """The core graphical object representation of the staff.

        This property is read-only.
        """
        return self._grob

    @property
    def pos(self):
        """Point: The position of the staff.

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self._pos

    @property
    def x(self):
        """GraphicUnit: x coordinate of the left side of the staff.

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self.pos.x

    @property
    def y(self):
        """GraphicUnit: y coordinate of the left side of the staff.

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self.pos.x

    @property
    def length(self):
        """GraphicUnit: length coordinate of the left side of the staff.

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self._length

    @property
    def height(self):
        """GraphicUnit: The height of the staff from top to bottom line.

        If the staff only has one line, its height is defined as 0.

        This property is read-only.
        """
        return (self.line_count - 1) * self.staff_unit

    @property
    def line_count(self):
        """int: The number of lines in the staff

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self._line_count

    @property
    def contents(self):
        """list[StaffObject]: A list of staff objects belonging to the staff

        This property is read-only. TODO: Low priority: implement setter?
        """
        return self._contents

    @property
    def highest_position(self):
        """int: The staff position of the top line

        This property is read-only
        """
        return self.line_count - 1

    @property
    def lowest_position(self):
        """int: The staff position of the bottom line

        This property is read-only.
        """
        return (self.line_count - 1) * -1

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

    def _staff_pos_to_rel_pixels(self, staff_position):
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
        return ((self.staff_unit / 2) *
                self._staff_pos_to_top_down(staff_position))

    def _position_inside_staff(self, position):
        """bool: Determine if a position is inside the staff.

        This is true for any position within or on the outer lines.
        """
        return self.lowest_position <= position <= self.highest_position

    def _position_outside_staff(self, position):
        """bool: Determine if a position is outside of the staff.

        This is true for any position not on or between the outer staff lines.
        """
        return not self._position_inside_staff(position)

    def _position_on_ledger(self, position):
        """bool: Tell if a position is on a ledger line position"""
        # If the position is outside the staff and self.count_count and
        # position's evenness are different, a ledger line is needed
        return (self._position_outside_staff(position) and
                self.line_count % 2 != position % 2)

    def _ledgers_needed_from_position(self, position):
        """set{int}: Ledgers needed for a note at a given position."""
        direction = 1 if position < 0 else -1
        if position is None or self._position_inside_staff(position):
            return set()
        else:
            # Find start and end points for ledger generation
            start = position
            if not self._position_on_ledger(position):
                start += direction
            if direction == 1:
                end = self.lowest_position
            else:
                end = self.highest_position
            return {pos for pos in range(start, end, 2 * direction)}

    def _register_staff_object(self, staff_object):
        """Add a StaffObject to `self.contents`.

        Args:
            staff_object (StaffObject): The object to add to `self.contents`

        Warning:
            This does not set `staff_object.staff` to self"""
        self._contents.append(staff_object)
        staff_object.staff = self
