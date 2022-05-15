from __future__ import annotations

from functools import reduce
from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.directions import DirectionY
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import PenDef
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.rect import Rect
from neoscore.core.repeating_music_text_line import RepeatingMusicTextLine
from neoscore.western.chordrest import Chordrest


class ArpeggioLine(RepeatingMusicTextLine):

    """An arpeggio roll line, optionally with an arrow.

    This is a thin convenience wrapper around ``RepeatingMusicTextLine``.
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
                must implement :obj:`.HasMusicFont`.
            end_pos: The stopping point.
            end_parent: The parent for the ending position.
                If ``None``, defaults to ``self``.
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
            None,
            end_cap_text,
            font,
            brush,
            pen,
            background_brush,
        )

    @classmethod
    def for_chord(
        cls,
        chordrest: Chordrest,
        arrow_direction: Optional[DirectionY] = None,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        background_brush: Optional[BrushDef] = None,
    ) -> ArpeggioLine:
        """Convenience constructor for an arpeggio line attached to a chord.

        Args:
            chordrest: The chord to attach the line to. This must not be a rest.
            arrow_direction: If provided, cap the line with an arrow pointing this way.
            font: A font override. If omitted, the chord's font is used.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            background_brush: Optional brush used to paint the text's bounding rect
                behind it.
        """
        if font:
            unit = font.unit
        else:
            unit = chordrest.staff.unit
        # Merge the bounding rects of all accidentals and noteheads
        # (offset relative to chordrest)
        guide_rect = reduce(
            lambda a, b: a.merge(b),
            [n.bounding_rect.offset(n.pos) for n in chordrest.noteheads],
        )
        if chordrest.accidentals:
            accidental_rect = reduce(
                lambda a, b: a.merge(b),
                [a.bounding_rect.offset(a.pos) for a in chordrest.accidentals],
            )
            guide_rect = Rect(
                accidental_rect.x, guide_rect.y, guide_rect.width, guide_rect.height
            )
        top = Point(guide_rect.x - unit(0.5), guide_rect.y - unit(0.25))
        bottom = Point(top.x, top.y + guide_rect.height + unit(0.5))
        include_arrow = arrow_direction is not None
        if arrow_direction == DirectionY.UP:
            start = bottom
            end = top
        else:
            start = top
            end = bottom
        return ArpeggioLine(
            start,
            chordrest,
            end,
            chordrest,
            include_arrow,
            font,
            brush,
            pen,
            background_brush,
        )
