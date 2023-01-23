from __future__ import annotations

from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.western.chordrest import Chordrest


class Tremolo(MusicText):

    """A tremolo marking over a single Chordrest.

    This uses basic tremolo glyphs e.g. tremolo3.
    If specific tremolo's are required e.g. penderecki, a workaround is:
    MusicText(cr.mid_stem_attachment_point(), cr, 'pendereckiTremolo').

    If a bridging tremolo is required between two Chordrests,
    then move the x position with the pos variable.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        strokes: int,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos: The starting (left) position of the beam
            parent: The parent for the starting position, must be a Chordrest. If no font is given, this or one of its ancestors must
                implement :obj:`.HasMusicFont`.
            strokes: number of strokes indicated in the tremolo. Must be 1, 2, 3, 4 or 5
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """

        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_font = font

        if 1 > strokes > 5:
            raise AttributeError("Invalid stroke number: {}".format(strokes))
        tremolo_smufl_name = "tremolo" + str(strokes)

        MusicText.__init__(self, pos, parent, tremolo_smufl_name, font, brush, pen)

    # todo - properties

    @classmethod
    def for_chordrest(self, cr: Chordrest, strokes: int) -> Tremolo:
        trem_pos = cr.mid_stem_attachment_point()
        Tremolo(trem_pos, cr, strokes)
