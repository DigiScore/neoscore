from __future__ import annotations

from typing import Optional

from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject


class RhythmDot(MusicText):

    """A single rhythmic dot"""

    _glyph_name = "augmentationDot"

    def __init__(
        self, pos: PointDef, parent: PositionedObject, font: Optional[MusicFont] = None
    ):
        """
        Args:
            pos: Position relative to `parent`
            parent: If no font is given, this or one of its ancestors must
                implement `HasMusicFont`.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        MusicText.__init__(self, pos, parent, [self._glyph_name], font)
