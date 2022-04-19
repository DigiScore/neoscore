from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, cast

from neoscore.core.exceptions import NoClefError
from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit, make_unit_class
from neoscore.western.octave_line import OctaveLine
from neoscore.western.transposition import Transposition

if TYPE_CHECKING:
    from neoscore.western.clef import Clef


class Staff(MusicPath):
    """A staff with decently high-level knowledge of its contents."""

    # Type sentinel used to hackily check if objects are Staff
    # without importing the type, risking cyclic imports.
    _neoscore_staff_type_marker = True

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        length: Unit,
        line_spacing: Unit = Mm(1.75),
        line_count: int = 5,
        music_font_family: str = "Bravura",
        pen: Optional[Pen] = None,
    ):
        """
        Args:
            pos: The position of the top-left corner of the staff
            parent: The parent for the staff. Make this a ``Flowable``
                to allow the staff to run across line and page breaks.
            length: The horizontal width of the staff
            line_spacing: The distance between two lines in the staff.
            line_count: The number of lines in the staff.
            music_font_family: The name of the font to use for MusicText objects
                in the staff. This defaults to the system-wide default music font
                family.
            pen: The pen used to draw the staff lines. Defaults to a line with
                thickness from the music font's engraving default.
        """
        unit = self._make_unit_class(line_spacing)
        music_font = MusicFont(music_font_family, unit)
        pen = pen or Pen(thickness=music_font.engraving_defaults["staffLineThickness"])
        super().__init__(pos, parent, font=music_font, pen=pen)
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
    def center_y(self) -> Unit:
        """The position of the center staff position"""
        return self.height / 2

    @property
    def barline_extent(self) -> tuple[Unit, Unit]:
        """The starting and stopping Y positions of barlines in this staff.

        For staves with more than 1 line, this extends from the top line to bottom
        line. For single-line staves, this extends from 1 unit above and below the
        staff.
        """
        if self.line_count == 1:
            return self.unit(-1), self.unit(1)
        else:
            return self.unit(0), self.unit(0) # self.height

    @property
    def breakable_length(self) -> Unit:
        # Override expensive ``Path.length`` since the staff length here
        # is already known.
        return self._length

    ######## PUBLIC METHODS ########

    def distance_to_next_of_type(self, staff_object: PositionedObject) -> Unit:
        """Find the x distance until the next occurrence of an object's type.

        If the object is the last of its type, this gives the remaining length
        of the staff after the object.

        This is useful for determining rendering behavior of staff objects
        which are active until another of their type occurs,
        such as ``KeySignature`` and ``Clef``.
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
            return self.breakable_length - start_x
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
            if line_pos <= pos_x <= line_pos + item.breakable_length:
                return item.transposition
        return None

    def middle_c_at(self, pos_x: Unit) -> Unit:
        """Find the y-axis staff position of middle-c at a given point.

        Looks for clefs and other transposing modifiers to determine
        the position of middle-c.

        If no clef is present, a ``NoClefError`` is raised.
        """
        clef = self.active_clef_at(pos_x)
        if clef is None:
            raise NoClefError
        transposition = self.active_transposition_at(pos_x)
        if transposition:
            return clef.middle_c_staff_position - self.unit(
                transposition.interval.staff_distance
            )
        else:
            return clef.middle_c_staff_position

    def y_inside_staff(self, pos_y: Unit) -> bool:
        """Determine if a y-axis position is inside the staff.

        This is true for any position within or on the outer lines.
        """
        return ZERO <= pos_y <= self.height

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
