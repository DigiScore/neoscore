from __future__ import annotations

from typing import Optional, cast

from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit, make_unit_class

_LINE_SPACE_TO_FONT_UNIT_RATIO: float = 2 / 3


class TabStaff(MusicPath):
    """A staff for writing guitar tablature with any number of strings.

    This class is not suitable for use with `Chordrest`, `Clef`,
    `TimeSignature`, and other such classes dependent on classical
    staff semantics.

    While `TabStaff` has a `MusicFont`, its unit does not necessarily
    correspond to the distance between staff lines. By default, the
    line spacing is wider than classical staves, and its `MusicFont`
    is sized to 2/3 that spacing.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        length: Unit,
        line_spacing: Unit = Mm(2.5),
        line_count: int = 6,
        music_font: Optional[MusicFont] = None,
        pen: Optional[Pen] = None,
    ):
        """
        Args:
            pos: The position of the top-left corner of the staff
            parent: The parent for the staff. Make this a `Flowable`
                to allow the staff to run across line and page breaks.
            length: The horizontal width of the staff
            line_spacing: The distance between two lines in the staff.
            line_count: The number of lines in the staff.
            music_font: The font to use for `MusicText` objects in the staff.
                Unlike in `Staff`, this font's `unit` is not necessarily equivalent
                to the space between two staff (string) lines. By default, this will
                use the system-wide default music font with a unit sized to 2/3 the
                staff line spacing.
            pen: The pen used to draw the staff lines. Defaults to a line with
                thickness from the music font's engraving default.
        """
        music_font = music_font or MusicFont(
            "Bravura",
            make_unit_class(
                "TabStaffTextUnit",
                line_spacing.base_value * _LINE_SPACE_TO_FONT_UNIT_RATIO,
            ),
        )
        pen = pen or Pen(thickness=music_font.engraving_defaults["staffLineThickness"])
        super().__init__(pos, parent, font=music_font, pen=pen)
        self._line_spacing = line_spacing
        self._line_count = line_count
        self._length = length
        for i in range(self.line_count):
            y_offset = self.line_spacing * i
            self.move_to(ZERO, y_offset)
            self.line_to(length, y_offset)

    def string_y(self, string: int) -> Unit:
        """Return the Y position of a given string's line.

        Strings are indicated from 1 to N, where 1 is the top string
        and N is the bottom.
        """
        return self.line_spacing * (string - 1)

    @property
    def height(self) -> Unit:
        """The height of the staff from top to bottom line.

        If the staff only has one line, its height is defined as 0.
        """
        return self.line_spacing * (self.line_count - 1)

    @property
    def line_count(self) -> int:
        """The number of lines in the staff"""
        return self._line_count

    @property
    def line_spacing(self) -> Unit:
        """The distance between two lines in the staff.

        Note that this is typically *not* `TabStaff.unit(1)`.
        """
        return self._line_spacing

    @property
    def center_y(self) -> Unit:
        """The position of the center staff position"""
        return cast(Unit, self.height / 2)

    @property
    def breakable_length(self) -> Unit:
        # Override expensive `Path.length` since the staff length here
        # is already known.
        return self._length

    @property
    def font_to_staff_space_ratio(self) -> float:
        return cast(float, self.unit(1) / self.line_spacing)
