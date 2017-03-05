from brown.config import config
from brown.core.music_font import MusicFont
from brown.core.path import Path
from brown.models.beat import Beat
from brown.models.container import Container
from brown.primitives.chordrest import ChordRest
from brown.primitives.clef import Clef
from brown.primitives.time_signature import TimeSignature
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Unit


class NoClefError(Exception):
    """Exception raised when no clef is present in a Staff where needed"""
    pass


class Staff(Path):
    """A staff capable of holding `StaffObject`s"""

    _whole_note_size = 8  # StaffUnits

    def __init__(self, pos, width, frame,
                 staff_unit=None, line_count=5, music_font=None,
                 default_time_signature_duration=None):
        """
        Args:
            pos (Point): The position of the top-left corner of the staff
            width (Unit): The horizontal width of the staff
            staff_unit (Unit): The distance between two lines in the staff.
                If not set, this will default to config.DEFAULT_STAFF_UNIT
            line_count (int): The number of lines in the staff.
            music_font (MusicFont): The font to be used in all
                MusicTextObjects unless otherwise specified.
            default_time_signature_duration (tuple or None): The duration tuple
                of the initial time signature. If none, (4, 4) will be used.
        """
        super().__init__(pos, parent=frame)
        self._line_count = line_count
        self._width = width
        self.unit = self._make_unit_class(staff_unit if staff_unit
                                          else config.DEFAULT_STAFF_UNIT)
        self.beat = Beat.make_concrete_beat(self.unit(40))
        if music_font is None:
            self.music_font = MusicFont(config.DEFAULT_MUSIC_FONT_NAME,
                                        self.unit)
        # Construct the staff path
        for i in range(self.line_count):
            y_offset = self.unit(i)
            self.move_to(GraphicUnit(0), y_offset)
            self.line_to(width, y_offset)

        # Create first measure with given time signature duration
        self._contents = Container()
        if default_time_signature_duration:
            self.default_time_signature_duration = self.beat(
                default_time_signature_duration)
        else:
            self.default_time_signature_duration = self.beat(4, 4)

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
        """Container[GraphicObject]: The collection of objects in the staff"""
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

    # Object adder methods ----------------------------------------------------

    def add_clef(self, time, clef_type):
        """Add a clef.

        Args:
            time (Beat tuple):
            clef_type (str): One of: 'treble', 'bass', '8vb bass',
                'tenor', or 'alto'

        Returns: None
        """
        pos_x = self.beat(*time)
        self.contents.append(Clef(self, pos_x, clef_type))

    def add_time_signature(self, measure_number, duration):
        """Add a time signature.

        Args:
            measure_number (int): The bar number
            duration (Beat tuple): The length of a measure in this
                time signature. The numerator and denominators
                of this duration are used literally as the numbers
                in the rendered representation of the signature.
                While a 6/8 measure will take the same amount of time
                as a 3/4 measure, the representations (and note groupings)
                are different.

        Returns: None
        """
        pos_x = self.beat(measure_number, 1)
        duration = self.beat(*duration)
        self.contents.append(TimeSignature(pos_x, duration, self))

    def add_chordrest(self, time, pitches, duration):
        """
        Args:
            time (Beat tuple):
            pitches (list[str]):
            duration (Beat tuple):
        """
        # See notes in self.add_clef about the hacks used here
        pos_x = self.beat(*time)
        duration = self.beat(*duration)
        self.contents.append(ChordRest(pos_x, self, pitches, duration))

    # Other methods -----------------------------------------------------------

    def active_clef_at(self, pos_x):
        """Find and return the active clef at a given x position.

        pos_x (Unit):

        Returns: Clef
        """
        # TODO: Implement a more efficient way to quickly look up contents by type
        if self.contents:
            return max([item for item in self.contents if item.x < pos_x],
                       key=lambda item: item.x)
        else:
            return None

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
            _conversion_rate = float(Unit(staff_unit_size))
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
