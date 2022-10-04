from __future__ import annotations

from typing import Optional, cast

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.directions import DirectionY
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.point import ORIGIN, Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner
from neoscore.core.units import Unit

_GLYPHS = {
    "15ma": "quindicesimaAlta",
    "8va": "ottavaAlta",
    "8vb": "ottavaBassaVb",
    "15mb": "quindicesimaBassaMb",
    "(": "octaveParensLeft",
    ")": "octaveParensRight",
}


class OctaveLine(PositionedObject, Spanner, HasMusicFont):

    """An octave indication with a dashed line.

    This octave line is purely cosmetic, and does not result in any automatic
    transpositions.

    At the starting position the octave is written in text, followed by a dashed line
    ending in a small vertical hook pointing toward the staff. If the spanner goes
    across line breaks, the octave text is repeated in parentheses at the line
    beginning.
    """

    def __init__(
        self,
        start: PointDef,
        start_parent: PositionedObject,
        end_x: Unit,
        end_parent: Optional[PositionedObject] = None,
        indication: str = "8va",
        direction: DirectionY = DirectionY.DOWN,
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

                    * '15ma' (two octaves higher)
                    * '8va' (one octave higher)
                    * '8vb' (one octave lower)
                    * '15mb' (two octaves lower)

            direction: The direction the line's ending hook points.
                For lines above staves, this should be down, and vice versa for below.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        PositionedObject.__init__(self, start, start_parent)
        Spanner.__init__(self, end_x, end_parent or self)
        if font is None:
            font = HasMusicFont.find_music_font(start_parent)
        self._music_font = font
        self.direction = direction

        self.line_path = Path(
            ORIGIN,
            self,
            Brush.no_brush(),
            Pen(
                thickness=font.engraving_defaults["octaveLineThickness"],
                pattern=PenPattern.DASH,
            ),
        )

        self.line_text = _OctaveLineText(
            ORIGIN, self, self.breakable_length, indication, font
        )

        # Vertically center the path relative to the text
        text_rect = self.line_text.bounding_rect
        path_x = text_rect.width
        path_y = cast(Unit, text_rect.height / -2)
        self.line_path.pos = Point(path_x, path_y)

        # Drawn main line part
        self.line_path.line_to(self.end_pos.x, path_y, self.end_parent)
        self.line_path.line_to(
            self.end_pos.x,
            (path_y + font.unit(0.75 * self.direction.value)),
            self.end_parent,
        )

    @property
    def music_font(self) -> MusicFont:
        return self._music_font


class _OctaveLineText(MusicText):
    """An octave text mark recurring at line beginnings with added parenthesis.

    This is a private class meant to be used exclusively in the context
    of an OctaveLine
    """

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        length: Unit,
        indication: str,
        font: MusicFont,
    ):
        super().__init__(
            pos,
            parent,
            _GLYPHS[indication],
            font,
            background_brush=neoscore.background_brush,
        )
        open_paren_char = MusicChar(self.music_font, _GLYPHS["("])
        close_paren_char = MusicChar(self.music_font, _GLYPHS[")"])
        self.parenthesized_text = (
            open_paren_char.codepoint + self.text + close_paren_char.codepoint
        )
        self._length = length

    @property
    def breakable_length(self) -> Unit:
        return self._length

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        super().render_complete(pos, flowable_line)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        super().render_complete(pos, flowable_line)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        super().render_complete(pos, flowable_line)
