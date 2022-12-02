from __future__ import annotations

from typing import List, Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.directions import DirectionY
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.text_alignment import AlignmentX, AlignmentY
from neoscore.core.units import ZERO


class Tuplet(PositionedObject, Spanner2D, HasMusicFont):
    """A polyrhythm indicator such as triplet or 3:4.

    This tuplet indicator spans a group of notes labelling them
    as triplet or more complex polyrhythms such as 5:4.

    At the centre of this line is the tuplet number.
    More complex ratios can be declared
    such as 7:8, 11:16, 12:14.

    Optional parameters enable bracket visibility,
    and bracket direction.

    """

    def __init__(
        self,
        start: PointDef,
        start_parent: PositionedObject,
        end: PointDef,
        end_parent: Optional[PositionedObject] = None,
        indicator_text: str = "3",
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
            indicator_text: The tuplet indicator text drawn at the middle of the spanner.
                This should contain only of numbers and colons, for example "3" or "5:4".
                Any other character will cause a ``ValueError`` to be raised.
            include_bracket: Whether to draw a bracket spanning the tuplet
            bracket_dir: The direction the line's ending hook points.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        PositionedObject.__init__(self, start, start_parent)
        Spanner2D.__init__(self, end, end_parent or self)
        if font is None:
            font = HasMusicFont.find_music_font(start_parent)
        self._music_font = font
        self.direction = bracket_dir

        # Calculate the bracket end length
        self.bracket_height = self.music_font.unit(self.direction.value)

        # Create bracket path if needed
        self.bracket: Optional[Path] = (
            self._create_bracket() if include_bracket else None
        )

        # Convert ratio text to SMuFL glyphs
        self.smufl_text = self._indicator_to_glyph_names(indicator_text)

        # Create line text object; will paint over bracket line
        spanner_center = self.point_along_spanner(0.5)
        self.indicator = MusicText(
            (spanner_center.x, spanner_center.y + self.bracket_height),
            self,
            self.smufl_text,
            font,
            background_brush=neoscore.background_brush,
            alignment_x=AlignmentX.CENTER,
            alignment_y=AlignmentY.CENTER,
        )

    def _create_bracket(self) -> Path:
        bracket = Path(
            ORIGIN,
            self,
            Brush.no_brush(),
            Pen(thickness=self.music_font.engraving_defaults["tupletBracketThickness"]),
        )
        # Draw opening crook
        bracket.line_to(ZERO, self.bracket_height)
        # Draw spanning line
        bracket.line_to(
            self.end_pos.x, self.end_y + self.bracket_height, self.end_parent
        )
        # Draw end crook
        bracket.line_to(self.end_pos.x, self.end_y, self.end_parent)
        return bracket

    @staticmethod
    def _indicator_to_glyph_names(indicator: str) -> List[str]:
        """Converts indicator text to corresponding SMuFL names

        Args:
            number: the original ratio string
        """
        smufl_list = []
        for char in indicator:
            if char == ":":
                smufl_list.append("tupletColon")
            else:
                smufl_list.append(f"tuplet{char}")
        return smufl_list

    @property
    def music_font(self) -> MusicFont:
        return self._music_font
