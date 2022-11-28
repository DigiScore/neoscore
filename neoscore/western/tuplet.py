from __future__ import annotations

from typing import Optional, cast, List
from math import sqrt

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.directions import DirectionY
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, PointDef, Unit
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.spanner import Spanner


class Tuplet(PositionedObject, Spanner, HasMusicFont):
    """A polyrhythm indicator such as triplet or 3:4.

    This tuplet indicator spans a group of notes labelling them
    as triplet or more complex polyrhythms such as 5:4.

    Starting at the first event in the grouping (note or rest),
    the indicator spans across to the end event (note or rest).
    At the centre of this line is the tuplet number
    (default = 3 for triplet). More complex ratios can be declared
    such as 7:8, 11:16, 12:14.

    Optional parameters enable bracket visibility (default = True),
    and bracket direction (default = DOWN).

    It is not common music engraving practice to split tuplets
    across bar lines or staff splits, so this function is
    not supported.
    """

    def __init__(
        self,
        start: PointDef,
        start_parent: PositionedObject,
        end: Unit,
        end_parent: Optional[PositionedObject] = None,
        ratio_text: str = "3",
        include_bracket: bool = True,
        bracket_dir: DirectionY = DirectionY.DOWN,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            start: The starting point.
            start_parent: The parent for the starting position. If no font is given,
                this or one of its ancestors must implement :obj:`.HasMusicFont`.
            end_x: The spanner end x position. The y position will be
                automatically calculated to be horizontal.
            end_parent: An object either in a Staff or
                a staff itself. The root staff of this *must* be the same
                as the root staff of ``start_parent``. If omitted, the
                stop point is relative to the start point.
            indication: A valid octave indication. currently supported indications are:



            direction: The direction the line's ending hook points.
                For lines above staves, this should be down, and vice versa for below.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        PositionedObject.__init__(self, start, start_parent)
        Spanner.__init__(self, end, end_parent or self)
        if font is None:
            font = HasMusicFont.find_music_font(start_parent)
        self._music_font = font
        self.direction = bracket_dir
        self.end_x_adjustment = self.music_font.unit(1)

        # Create line path object
        self.line_path = Path(
            ORIGIN,
            self,
            Brush.no_brush(),
            Pen(thickness=font.engraving_defaults["tupletBracketThickness"]
                ),
        )

        # Calculate the bracket end length
        self.bracket_end = self.music_font.unit(1 * self.direction.value)
        # Draw bracket
        if include_bracket:
            self._draw_path()

        # Convert ratio text to SMuFL glyphs
        self.smufl_text = self._number_to_digit_glyph_names(ratio_text)

        # Create line text object; will paint over bracket line
        self.text_start_point = self._find_text_start_point()
        self.line_text = MusicText(
            self.text_start_point,
            self.parent,
            self.smufl_text,
            font,
            background_brush=neoscore.background_brush,
            # rotation=self.angle
        )

    def _draw_path(self):
        """Draw the path according to this object's attributes.

        Returns: None
        """
        # Draw opening crook
        self.line_path.line_to(self.music_font.unit(0), self.bracket_end)

        # draw full line
        self.line_path.line_to(self.end_pos.x + self.end_x_adjustment, self.end_y + self.bracket_end, self.end_parent)

        # Draw end crook
        self.line_path.line_to(self.end_pos.x + self.end_x_adjustment, self.end_y, self.end_parent)

    @staticmethod
    def _number_to_digit_glyph_names(number: str) -> List[str]:
        smufl_list = []
        for digit in number:
            if digit == ":":
                smufl_list.append("tupletColon")
            else:
                smufl_list.append(f"tuplet{digit}")
        return smufl_list

    def _find_text_start_point(self) -> tuple:
        # Find x & y for half-way hypotenuse
        start_parent = self.parent
        end_parent = self.end_parent
        parent_distance = start_parent.map_to(end_parent)
        print(parent_distance)

        mid_x = (parent_distance.x + self.end_x_adjustment) / 2
        mid_y = ((self.end_y - self.pos.y) + self.bracket_end) / 2 #+ self.bracket_end

        # adjust for length of ration text
        # todo - replace with glyph width count
        if len(self.smufl_text) > 1:
            for _ in self.smufl_text:
                mid_x -= self.music_font.unit(0.5)
            if mid_x.base_value % 2 == 0:
                mid_x += self.music_font.unit(0.5)
        return (self.x + mid_x, self.y + mid_y)

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

