from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, cast

from neoscore import constants
from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import DEFAULT_PEN, Pen
from neoscore.core.positioned_object import PositionedObject
from neoscore.models.transposition import Transposition
from neoscore.utils.exceptions import NoClefError
from neoscore.utils.point import PointDef
from neoscore.utils.units import ZERO, Unit, make_unit_class
from neoscore.western.octave_line import OctaveLine

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent
    from neoscore.western.clef import Clef


class Staff(MusicPath):
    """A staff capable of holding `StaffObject`s"""

    # Type sentinel used to hackily check if objects are Staff
    # without importing the type, risking cyclic imports.
    _neoscore_staff_type_marker = True

    # TODO HIGH this init signature works very differently than most
    # MusicPath and similar do. It can't inherit its font (and thus
    # size) from an ancestor music font and the way it takes a music
    # font *family* and staff_unit feels awkward. rework this soon, as
    # it's a disruptive breaking change.

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent],
        length: Unit,
        staff_unit: Optional[Unit] = None,
        line_count: int = 5,
        music_font_family: Optional[str] = None,
        pen: Optional[Pen] = None,
    ):
        """
        Args:
            pos: The position of the top-left corner of the staff
            parent: The parent for the staff. Make this a `Flowable`
                to allow the staff to run across line and page breaks.
            length: The horizontal width of the staff
            staff_unit: The distance between two lines in the staff.
                If not set, this will default to `constants.DEFAULT_STAFF_UNIT`
            line_count: The number of lines in the staff.
            music_font_family: The name of the font to use for MusicText objects
                in the staff. This defaults to the system-wide default music font
                family.
            pen: The pen used to draw the staff lines. Defaults to a line with
                thickness from the music font's engraving default.
        """
        unit = self._make_unit_class(
            staff_unit if staff_unit else constants.DEFAULT_STAFF_UNIT
        )
        music_font = MusicFont(
            music_font_family or constants.DEFAULT_MUSIC_FONT_NAME, unit
        )
        pen = Pen.from_existing(
            DEFAULT_PEN, thickness=music_font.engraving_defaults["staffLineThickness"]
        )
        super().__init__(pos, parent, pen=pen, font=music_font)
        self._line_count = line_count
        self._length = length
        # Construct the staff path
        for i in range(self.line_count):
            y_offset = self.unit(i)
            self.move_to(ZERO, y_offset)
            self.line_to(length, y_offset)

    ######## PUBLIC PROPERTIES ########

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

    def distance_to_next_of_type(self, staff_object: PositionedObject) -> Unit:
        """Find the x distance until the next occurrence of an object's type.

        If the object is the last of its type, this gives the remaining length
        of the staff after the object.

        This is useful for determining rendering behavior of `StaffObject`s
        who are active until another of their type occurs,
        such as `KeySignature`s, or `Clef`s.
        """
        start_x = map_between_x(self, cast(PositionedObject, staff_object))
        all_others_of_class = (
            item
            for item in self.descendants_of_exact_class(type(staff_object))
            if item != staff_object
        )
        closest_x = Unit(float("inf"))
        for item in all_others_of_class:
            relative_x = map_between_x(self, item)
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
            line_pos = map_between_x(self, item)
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

    def ledgers_needed_for_y(self, position: Unit) -> list[Unit]:
        """Find the y positions of all ledgers needed for a given y position"""
        # Work on positions as integers for simplicity
        start = int(self.unit(position).display_value)
        if start < 0:
            return [self.unit(pos) for pos in range(start, 0, 1)]
        elif start > self.line_count - 1:
            return [self.unit(pos) for pos in range(start, self.line_count - 1, -1)]
        else:
            return []

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
            for clef in self.descendants_with_attribute("middle_c_staff_position")
        ]
        result.sort(key=lambda tup: tup[0])
        return result

    def _pre_render_hook(self):
        self._clef_x_positions = self._compute_clef_x_positions()

    def _post_render_hook(self):
        self._clef_x_positions = None
