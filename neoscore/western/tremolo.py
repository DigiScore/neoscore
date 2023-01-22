from __future__ import annotations

from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import ORIGIN, ZERO
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner import Spanner
from neoscore.western.chordrest import Chordrest


class Tremolo(Spanner, MusicText, PositionedObject):
    """A tremolo marking over a single Chordrest or between two Chordrests"""

    def __init__(
        self,
        parent=Chordrest,
        strokes=int,  # todo - this is unneccesry if declaring own alt_glyph
        end_parent: Optional[Chordrest] = None,
        alt_glyph: str = None,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            parent: The parent for the starting position, must be a Chordrest. If no font is given, this or one of its ancestors must
                implement :obj:`.HasMusicFont`.
            strokes: number of strokes indicated in the tremolo. Must be 1, 2, 3, 4 or 5
            end_parent: The parent for 2nd Chordrest, must be a Chordrest (optional)
            alt_glyph: The SmUFL name of specified tremolo as a string e.g. "pendereckiTremolo"
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        PositionedObject.__init__(self, ORIGIN, parent)
        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_font = font

        # todo stem direction

        if alt_glyph:
            tremolo_smufl_name = alt_glyph
        else:
            if 1 > strokes > 5:
                raise AttributeError("Invalid stroke number: {}".format(strokes))
            tremolo_smufl_name = "tremolo" + str(strokes)

        if end_parent:
            Spanner.__init__(self, ZERO, end_parent)
            spanner_centre = self.point_along_spanner(0.5)
            trem_pos = (spanner_centre.x, spanner_centre.y + font.unit(3))
        else:
            trem_pos = (
                parent.highest_notehead.pos.x + font.unit(1),
                parent.highest_notehead.pos.y - font.unit(2),
            )

        MusicText.__init__(self, trem_pos, parent, tremolo_smufl_name, font, brush, pen)
