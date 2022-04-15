from __future__ import annotations

from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import PenDef
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.repeating_music_text_line import RepeatingMusicTextLine


class ArpeggioLine(RepeatingMusicTextLine):

    """An arpeggio roll line, optionally with an arrow.

    This is a thin convenience wrapper around `RepeatingMusicTextLine`.
    """

    _MAIN_GLYPH = "wiggleArpeggiatoUp"
    _ARROW_GLYPH = "wiggleArpeggiatoUpArrow"

    def __init__(
        self,
        start: PointDef,
        start_parent: Optional[PositionedObject],
        end_pos: PointDef,
        end_parent: Optional[PositionedObject],
        include_arrow: bool = False,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        background_brush: Optional[BrushDef] = None,
    ):
        """
        Args:
            start: The starting point.
            start_parent: If no font is given, this or one of its ancestors
                must implement `HasMusicFont`.
            end_pos: The stopping point.
            end_parent: The parent for the ending position.
                If `None`, defaults to `self`.
            include_arrow: Whether to end the line with an arrow. This will be
                attached to the end position pointing away from the starting position.
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            background_brush: Optional brush used to paint the text's bounding rect
                behind it.
        """
        end_cap_text = ArpeggioLine._ARROW_GLYPH if include_arrow else None
        super().__init__(
            start,
            start_parent,
            end_pos,
            end_parent,
            ArpeggioLine._MAIN_GLYPH,
            end_cap_text,
            font,
            brush,
            pen,
            background_brush,
        )
