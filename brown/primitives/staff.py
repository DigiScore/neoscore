import bisect

from brown.utils.units import GraphicUnit, Unit
from brown.utils.point import Point
from brown.config import config
from brown.primitives.clef import Clef
from brown.core.path import Path
from brown.core.music_font import MusicFont


class NoClefError(Exception):
    """Exception raised when no clef is present in a Staff where needed"""
    pass


class Staff(Path):
    """A staff capable of holding `StaffObject`s"""

    def __init__(self, pos, width, frame,
                 staff_unit=None, line_count=5, default_music_font=None):
        """
        Args:
            pos (Point): The position of the top-left corner of the staff
            width (Unit): The horizontal width of the staff
            staff_unit (Unit): The distance between two lines in the staff.
                If not set, this will default to config.DEFAULT_STAFF_UNIT
            line_count (int): The number of lines in the staff.
            default_music_font (MusicFont): The font to be used in all
                MusicGlyphs unless otherwise specified.
        """
        super().__init__(pos, parent=frame)
        self._line_count = line_count
        self._width = width
        self.unit = self._make_unit_class(staff_unit if staff_unit
                                          else config.DEFAULT_STAFF_UNIT)
        if default_music_font is None:
            self.default_music_font = MusicFont(config.DEFAULT_MUSIC_FONT_NAME,
                                                self.unit)
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
    def top_line_y(self):
        """StaffUnit: The position of the top staff line"""
        return self.unit(0)

    @property
    def center_pos_y(self):
        """StaffUnit: The position of the center staff position"""
        return self.unit((self.line_count - 1) / 2)

    @property
    def bottom_line_y(self):
        """StaffUnit: The position of the bottom staff line"""
        return self.unit((self.line_count - 1))

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
        the position of middle-c.

        If no clef is present, a `NoClefError` is raised.

        Returns: StaffUnit: A vertical staff position
        """
        clef = self.active_clef_at(position_x)
        if clef is None:
            raise NoClefError
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
            _unit_name_plural = 'staff_units'
            _base_units_per_self_unit = float(Unit(staff_unit_size))
            # (all other functionality implemented in Unit)
        return StaffUnit

    def _position_inside_staff(self, position):
        """Determine if a position is inside the staff.

        This is true for any position within or on the outer lines.

        Args:
            position (StaffUnit): A vertical staff position

        Returns: bool
        """
        return self.top_line_y <= position <= self.bottom_line_y

    def _position_outside_staff(self, position):
        """Determine if a position is outside of the staff.

        This is true for any position not on or between the outer staff lines.

        Args:
            position (StaffUnit): A vertical staff position

        Returns: bool
        """
        return not self._position_inside_staff(position)

    def _position_on_ledger(self, position):
        """Tell if a position is on a ledger line position

        This is true for any whole-number position outside of the staff

        Args:
            position (StaffUnit): A vertical staff position

        Returns: bool
        """
        return (self._position_outside_staff(position) and
                self.unit(position).value % 1 == 0)

    def _ledgers_needed_from_position(self, position):
        """Find the y positions of all ledgers needed for a given y position

        Args:
            position (StaffUnit): Any y-axis position

        Returns: set{StaffUnit}
        """
        # Work on positions as integers for simplicity, but return as StaffUnits
        start = int(self.unit(position).value)
        if start < 0:
            return set(self.unit(pos)
                       for pos in range(start, 0, 1))
        elif start > self.line_count - 1:
            return set(self.unit(pos)
                       for pos in range(start, self.line_count - 1, -1))
        else:
            return set()

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
