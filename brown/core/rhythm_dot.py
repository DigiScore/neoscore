from typing import Optional

from brown.core.graphic_object import GraphicObject
from brown.core.music_font import MusicFont
from brown.core.music_text import MusicText
from brown.core.staff_object import StaffObject
from brown.utils.point import PointDef


class RhythmDot(MusicText, StaffObject):

    """A single rhythmic dot"""

    _glyph_name = "augmentationDot"

    def __init__(
        self, pos: PointDef, parent: GraphicObject, font: Optional[MusicFont] = None
    ):
        MusicText.__init__(self, pos, [self._glyph_name], parent, font)
        StaffObject.__init__(self, parent)
