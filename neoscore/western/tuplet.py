from __future__ import annotations

from math import cos, sin
from typing import List, Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.directions import DirectionY
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, ZERO, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D


class Tuplet(PositionedObject, Spanner2D, HasMusicFont):
    """A polyrhythm indicator such as triplet or 3:4.

    This tuplet indicator spans a group of notes labelling them
    as triplet or more complex polyrhythms such as 5:4.

    Starting at the first event in the grouping (note or rest),
    the indicator spans across to the end event (note or rest).
    An error will be raised if the spanning is right to left.

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
        end: PointDef,
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
            end: The spanner end point position. This must be to the right of the start position
            end_parent: An object either in a Staff or
                a staff itself. The root staff of this *must* be the same
                as the root staff of ``start_parent``. If omitted, the
                stop point is relative to the start point.
            ratio_text: The Tuplet number (e.g. 3 for tripets) or Ratio number (e.g. 5:4 for polyrhythms)
            include_bracket: Bool to draw the spanning bracket over the tuplet
            bracket_dir: The direction the line's ending hook points.
                For lines above staves, this should be down, and vice versa for below.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        PositionedObject.__init__(self, start, start_parent)
        Spanner2D.__init__(self, end, end_parent or self)
        self._position_checker()
        if font is None:
            font = HasMusicFont.find_music_font(start_parent)
        self._music_font = font
        self.direction = bracket_dir

        # Create line path object
        self.line_path = Path(
            ORIGIN,
            self,
            Brush.no_brush(),
            Pen(thickness=font.engraving_defaults["tupletBracketThickness"]),
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
            rotation=self.angle,
        )

    def _position_checker(self):
        """Checks if the Tuplet travels left to right."""
        parent_distance = self.parent.map_to(self.end_parent)
        if self.end_x - self.x + parent_distance.x < ZERO:
            raise AttributeError("Invalid Tuplet start or end positions")

    def _draw_path(self):
        """Draw the path according to this object's attributes.

        Returns: None
        """
        # Draw opening crook
        self.line_path.line_to(ZERO, self.bracket_end)

        # draw full line
        self.line_path.line_to(
            self.end_pos.x, self.end_y + self.bracket_end, self.end_parent
        )

        # Draw end crook
        self.line_path.line_to(self.end_pos.x, self.end_y, self.end_parent)

    @staticmethod
    def _number_to_digit_glyph_names(number: str) -> List[str]:
        """Converts ratio text to corresponding SMuFL names

        Args:
            number: str: the original ratio string

        Returns:
            List: SMuFL names"""
        smufl_list = []
        for digit in number:
            if digit == ":":
                smufl_list.append("tupletColon")
            else:
                smufl_list.append(f"tuplet{digit}")
        return smufl_list

    def _find_text_start_point(self) -> tuple:
        """Positions ratio text centre on the mid-point
        of the bracket line.
        Returns: tuple of x, y points"""
        # Find x & y for half-way hypotenuse
        start_parent = self.parent
        end_parent = self.end_parent
        parent_distance = start_parent.map_to(end_parent)
        x_distance = parent_distance.x + self.x + self.end_x
        y_distance = parent_distance.y + self.y + self.end_y

        mid_x = x_distance / 2
        mid_y = y_distance / 2 + self.bracket_end

        # print(self.line_text.bounding_rect)
        # centre_text_box_x = text_rect[2] / 2
        # centre_text_box_y = text_rect[3] / 2
        #
        # mid_x += centre_text_box_x
        # mid_y += centre_text_box_y


        # Centre ratio text with bracket direction DOWN
        # if self.direction == DirectionY.UP:
        #     mid_y += self.music_font.unit(0.5)
        # else:
        #     mid_y += self.music_font.unit(1)

        # adjust mid-points for length of ratio text
        num_digits = len(self.smufl_text)

        # for each digit move mid-point back along hypotenuse
        for digit in range(num_digits):
            print(self.angle)
            if self.angle >= 0:
                theta = self.angle
                # move adjacent and opposite coords by 0.5 unit on hypotenuse
                mid_x -= self.music_font.unit(0.5 * cos(theta))
                mid_y -= self.music_font.unit(0.5 * sin(theta))
            else:
                theta = self.angle * -1
                # move adjacent and opposite coords by 0.5 unit on hypotenuse
                mid_x -= self.music_font.unit(0.5 * cos(theta))
                mid_y += self.music_font.unit(0.5 * sin(theta))

        return (mid_x, mid_y)


    @property
    def music_font(self) -> MusicFont:
        return self._music_font
