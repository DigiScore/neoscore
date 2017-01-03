import bisect

from brown.utils.units import GraphicUnit, Unit
from brown.utils.point import Point
from brown.config import config
from brown.primitives.clef import Clef
from brown.core.path import Path


class Staff(Path):
    """A staff capable of holding `StaffObject`s"""

    def __init__(self, pos, width, frame, staff_unit=None, line_count=5):
        """
        Args:
            pos (Point): The position of the top-left corner of the staff
            width (Unit): The horizontal width of the staff
            staff_unit (Unit): The distance between two lines in the staff.
                If not set, this will default to config.DEFAULT_STAFF_UNIT
            line_count (int): The number of lines in the staff.
        """
        super().__init__(pos, parent=frame)
        self._line_count = line_count
        self._width = width
        self.unit = self._make_unit_class(staff_unit if staff_unit
                                          else config.DEFAULT_STAFF_UNIT)
        self._contents = []
        # Construct the staff path
        for i in range(self.line_count):
            y_offset = self.unit(i)
            self.move_to(Point(GraphicUnit(0), y_offset) + self.pos)
            self.line_to(Point(width, y_offset) + self.pos)

    ######## PUBLIC PROPERTIES ########

    @property
    def height(self):
        """GraphicUnit: The height of the staff from top to bottom line.

        If the staff only has one line, its height is defined as 0.

        This property is read-only.
        """
        return self.unit(self.line_count - 1)

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
        clef = None
        for item in self.contents:
            if item.x >= position_x:
                break
            if isinstance(item, Clef):
                clef = item
        return clef

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

    ######## PRIVATE METHODS ########

    @staticmethod
    def _make_unit_class(staff_unit_size):
        """Create a Unit class with a ratio of 1 to a staff unit size

        Args:
            staff_unit_size

        Returns:
            type: A new StaffUnit class specifically for use in this staff.
        """
        class StaffUnit(Unit):
            _unit_name_plural = 'mm'
            _base_units_per_self_unit = float(Unit(staff_unit_size))
            # (all other functionality implemented in Unit)
        return StaffUnit

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
        return float(GraphicUnit(self.unit(
            self._staff_pos_to_top_down(centered_value))))

    # TODO: Implement more functions breaking apart the translation of staff
    #       space to flowable space.

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
        # Maintain contents in sorted order
        # TODO: Implement a more efficient structure/algorithm for this
        self._contents.sort(key=lambda val: val.x)
