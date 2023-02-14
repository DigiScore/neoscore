from __future__ import annotations

from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.directions import DirectionY
from neoscore.core.music_font import MusicFont
from neoscore.core.pen import PenDef
from neoscore.core.point import PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.units import Unit
from neoscore.western.abstract_slur import AbstractSlur


class Slur(Spanner2D, AbstractSlur):

    """A slur, conventionally drawn between notes.

    Note that this class currently provides no smart positioning logic to automatically
    attach to and span between :obj:`.Chordrest`\ s.

    For ties, see :obj:`.Tie`, which works identically to this class except that it
    always spans horizontally.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        end_pos: PointDef,
        end_parent: Optional[PositionedObject] = None,
        direction: DirectionY = DirectionY.UP,
        height: Optional[Unit] = None,
        arch_length: Optional[Unit] = None,
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos: The starting point.
            parent: The parent for the starting position. If no font is provided,
                this parent or one of its ancestors must implement :obj:`.HasStaffUnit`.
            end_pos: The stopping point.
            end_parent: The parent for the ending position.
                If ``None``, defaults to ``self``.
            direction: The vertical direction the slur arches.
            height: The ascent or descent of the curve given in absolute value.
                If omitted, a reasonable default is derived from other properties.
            arch_length: The x-offset of the outer ascent or descent curve control points.
                Smaller values give tighter arches. If omitted, a reasonable default is
                derived from other properties
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        AbstractSlur.__init__(
            self, pos, parent, direction, height, arch_length, font, brush, pen
        )
        Spanner2D.__init__(self, end_pos, end_parent or self)
        self.draw_slur(self.end_pos, self.end_parent)
