from __future__ import annotations

from typing import Optional

from neoscore.core.brush import BrushDef
from neoscore.core.directions import DirectionY
from neoscore.core.math_helpers import interpolate
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import PenDef
from neoscore.core.point import ORIGIN, Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.units import ZERO, Unit
from neoscore.western.abstract_slur import AbstractSlur



class Tie(AbstractSlur, MusicPath, Spanner2D):

    """A tie.

    While this is a path, it requires a music font from which to derive its appearance.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        end_x: Point,
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
        MusicPath.__init__(self, pos, parent, font, brush, pen)

        end_pos = Point(end_x, ZERO)
        Spanner2D.__init__(self, end_pos, end_parent or self)
        self.direction = direction
        self.height = height
        self.arch_length = arch_length
        # Load relevant engraving defaults from music font
        self.midpoint_thickness = self.music_font.engraving_defaults[
            "slurMidpointThickness"
        ]
        self.endpoint_thickness = self.music_font.engraving_defaults[
            "slurEndpointThickness"
        ]
        self.length = self.spanner_2d_length
        # Work out parameters
        # self.abs_height = self.height if self.height else self._derive_height()
        # self.arch_length = (
        #     self.arch_length if self.arch_length else self._derive_arch_length()
        # )
        # self.mid_height = self.abs_height * self.direction.value
        # self.mid_upper_height = self.mid_height + (self.midpoint_thickness * self.direction.value)
        # self.end_height = self.endpoint_thickness * self.direction.value

        # draw slur
        AbstractSlur.draw_slur(self)