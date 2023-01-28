from __future__ import annotations

from typing import Optional, Union

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

    The tremolo indicator accepts either an integer for declaring the number
    of strokes of a combining (common) tremolo, or a
    SMuFL glyphname e.g. "pendereckiTremolo".

    If a bridging tremolo is required between two Chordrests,
    then move the x position with the pos variable.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        indication: Union[int, str],
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos: The starting position
            parent: The parent for the starting position. If no font is given, this or one of its ancestors must
                implement :obj:`.HasMusicFont`.
            indication: The type of tremolo to draw, either a stroke count for conventional
                tremolos (1-5) or an arbitrary SMuFL glyphname.
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """

        if font is None:
            font = HasMusicFont.find_music_font(parent)
        self._music_font = font
        self.pos = pos

        if isinstance(indication, int):
            if 1 > indication > 5:
                raise ValueError("Invalid stroke number: {}".format(indication))
            self.tremolo_smufl_name = "tremolo" + str(indication)
        else:
            self.tremolo_smufl_name = indication

        MusicText.__init__(
            self, self.pos, parent, self.tremolo_smufl_name, font, brush, pen
        )

    @classmethod
    def for_chordrest(
        cls,
        chordrest: Chordrest,
        indication: Union[int, str],
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ) -> Tremolo:
        """Convenience constructor for a tremolo attached to a chord

        Args:
           chordrest: The chord to attach the tremolo to.
           indication: The type of tremolo to draw, either a stroke count for conventional
                tremolos (1-5) or an arbitrary SMuFL glyphname.
           font: If provided, this overrides any font found in the ancestor chain.
           brush: The brush to fill shapes with.
           pen: The pen to draw outlines with.
        """

        trem_pos = chordrest.tremolo_attachment_point()

        return Tremolo(trem_pos, chordrest, indication, font, brush, pen)

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    @property
    def glyph_name(self) -> str:
        return self.tremolo_smufl_name

    @property
    def tremolo_position(self) -> PointDef:
        return self.pos
