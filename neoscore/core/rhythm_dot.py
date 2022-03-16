from typing import Optional

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.staff_object import StaffObject
from neoscore.utils.point import PointDef


class RhythmDot(MusicText, StaffObject):

    """A single rhythmic dot"""

    _glyph_name = "augmentationDot"

    def __init__(
        self, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ):
        MusicText.__init__(self, pos, parent, [self._glyph_name], font)
        StaffObject.__init__(self, parent)
