from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

from brown import constants
from brown.core.clef import Clef
from brown.core.music_font import MusicFont
from brown.core.octave_line import OctaveLine
from brown.core.path import Path
from brown.models.beat import Beat
from brown.models.transposition import Transposition
from brown.utils.exceptions import NoClefError
from brown.utils.units import ZERO, Unit, make_unit_class

if TYPE_CHECKING:
    from brown.core.staff_object import StaffObject


class Staff(Path):
    """A staff capable of holding `StaffObject`s"""

    _whole_note_size = 8  # StaffUnits

    def __init__(
        self,
        pos,
        length,
        flowable,
        staff_unit=None,
        line_count=5,
        music_font=None,
        default_time_signature_duration=None,
        pen=None,
    ):
        """
        Args:
            pos (Point): The position of the top-left corner of the staff
            length (Unit): The horizontal width of the staff
            staff_unit (Unit): The distance between two lines in the staff.
                If not set, this will default to `constants.DEFAULT_STAFF_UNIT`
            line_count (int): The number of lines in the staff.
            music_font (MusicFont): The font to be used in all
                MusicTextObjects unless otherwise specified.
            default_time_signature_duration (tuple or None): The duration tuple
                of the initial time signature. If none, (4, 4) will be used.
            pen: The pen used to draw the staff lines. If none, a default solid
                black line is used.
        """
        super().__init__(pos, parent=flowable, pen=pen)
        self._line_count = line_count
        self._unit = self._make_unit_class(
            staff_unit if staff_unit else constants.DEFAULT_STAFF_UNIT
        )
        if music_font is None:
            self.music_font = MusicFont(constants.DEFAULT_MUSIC_FONT_NAME, self.unit)
        self._length = length
        # Construct the staff path
        for i in range(self.line_count):
            y_offset = self.unit(i)
            self.move_to(ZERO, y_offset)
            self.line_to(length, y_offset)

        # Create first measure with given time signature duration
        if default_time_signature_duration:
            self.default_time_signature_duration = Beat(default_time_signature_duration)
        else:
            self.default_time_signature_duration = Beat(4, 4)

    ######## PUBLIC PROPERTIES ########

    @property
    def unit(self) -> Type[Unit]:
        """A unit type where 1 is the distance between two staff lines.

        This is a generated class with the name `StaffUnit`. All `Staff`
        objects have a unique `StaffUnit` class such that different sized
        staves may coexist within a score and `StaffObject`s placed within
        them will be able to correctly position and scale themselves
        accordingly.

        This class is generated automatically according to `self.height`
        and `self.line_count`, with the assumption that all staff lines
        are evenly spaced.
        """
        return self._unit

    @property
    def height(self) -> Unit:
        """The height of the staff from top to bottom line.

        If the staff only has one line, its height is defined as 0.
        """
        return self.unit(self.line_count - 1)

    @property
    def line_count(self) -> int:
        """The number of lines in the staff"""
        return self._line_count

    @property
    def top_line_y(self) -> Unit:
        """The position of the top staff line"""
        return self.unit(0)

    @property
    def center_pos_y(self) -> Unit:
        """The position of the center staff position"""
        return self.unit((self.line_count - 1) / 2)

    @property
    def bottom_line_y(self) -> Unit:
        """The position of the bottom staff line"""
        return self.unit((self.line_count - 1))

    @property
    def length(self) -> Unit:
        # Override expensive `Path.length` since the staff length here
        # is already known.
        return self._length

    ######## PUBLIC METHODS ########

    def distance_to_next_of_type(self, staff_object: StaffObject) -> Unit:
        """Find the x distance until the next occurrence of an object's type.

        If the object is the last of its type, this gives the remaining length
        of the staff after the object.

        This is useful for determining rendering behavior of `StaffObject`s
        who are active until another of their type occurs,
        such as `KeySignature`s, or `Clef`s.
        """
        start_x = self.flowable.map_x_between_locally(self, staff_object)
        all_others_of_class = (
            item
            for item in self.descendants_of_exact_class(type(staff_object))
            if item != staff_object
        )
        closest_x = Unit(float("inf"))
        for item in all_others_of_class:
            relative_x = self.flowable.map_x_between_locally(self, item)
            if start_x < relative_x < closest_x:
                closest_x = relative_x
        if closest_x == Unit(float("inf")):
            return self.length - start_x
        return closest_x - start_x

    def clefs(self) -> list[tuple[Unit, Clef]]:
        """All the clefs in this staff, ordered by their relative x pos."""
        cached_clef_positions = getattr(self, "_clef_x_positions", None)
        if cached_clef_positions:
            return cached_clef_positions
        return self._compute_clef_x_positions()

    def active_clef_at(self, pos_x: Unit) -> Optional[Clef]:
        """Return the active clef at a given x position, if any."""
        clefs = self.clefs()
        return next(
            (clef for (clef_x, clef) in reversed(clefs) if clef_x <= pos_x),
            None,
        )

    def active_transposition_at(self, pos_x: Unit) -> Optional[Transposition]:
        """Return the active transposition at a given x position, if any."""
        for item in self.descendants_of_class_or_subclass(OctaveLine):
            line_pos = self.flowable.map_x_between_locally(self, item)
            if line_pos <= pos_x <= line_pos + item.length:
                return item.transposition
        return None

    def middle_c_at(self, pos_x: Unit) -> Unit:
        """Find the y-axis staff position of middle-c at a given point.

        Looks for clefs and other transposing modifiers to determine
        the position of middle-c.

        If no clef is present, a `NoClefError` is raised.
        """
        clef = self.active_clef_at(pos_x)
        if clef is None:
            raise NoClefError
        transposition = self.active_transposition_at(pos_x)
        if transposition:
            return clef.middle_c_staff_position + self.unit(
                transposition.interval.staff_distance
            )
        else:
            return clef.middle_c_staff_position

    def y_inside_staff(self, pos_y: Unit) -> bool:
        """Determine if a y-axis position is inside the staff.

        This is true for any position within or on the outer lines.
        """
        return self.top_line_y <= pos_y <= self.bottom_line_y

    def y_on_ledger(self, pos_y: Unit) -> bool:
        """Determine if a y-axis position is approximately at a ledger line position

        This is true for any whole-number staff position outside of the staff
        """
        return (not self.y_inside_staff(pos_y)) and self.unit(
            pos_y
        ).display_value % 1 == 0

    def ledgers_needed_for_y(self, position: Unit) -> set[Unit]:
        """Find the y positions of all ledgers needed for a given y position"""
        # Work on positions as integers for simplicity
        start = int(self.unit(position).display_value)
        if start < 0:
            return set(self.unit(pos) for pos in range(start, 0, 1))
        elif start > self.line_count - 1:
            return set(self.unit(pos) for pos in range(start, self.line_count - 1, -1))
        else:
            return set()

    ######## PRIVATE METHODS ########

    @staticmethod
    def _make_unit_class(staff_unit_size: Unit) -> Type[Unit]:
        """Create a Unit class with a ratio of 1 to a staff unit size

        Args:
            staff_unit_size

        Returns:
            type: A new StaffUnit class specifically for use in this staff.
        """

        return make_unit_class("StaffUnit", staff_unit_size.base_value)

    def _compute_clef_x_positions(self) -> list[tuple[Unit, Clef]]:
        result = [
            (clef.pos_x_in_staff, clef)
            for clef in self.descendants_of_class_or_subclass(Clef)
        ]
        result.sort(key=lambda tup: tup[0])
        return result

    def _pre_render_hook(self):
        self._clef_x_positions = self._compute_clef_x_positions()

    def _post_render_hook(self):
        self._clef_x_positions = None
