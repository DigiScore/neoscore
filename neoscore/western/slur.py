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


class Slur(MusicPath, Spanner2D):

    """A slur, also usable as a tie.

    While this is a path, it requires a music font from which to derive its appearance.
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
        MusicPath.__init__(self, pos, parent, font, brush, pen)
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
        self._draw_path()

    def _derive_height(self):
        length = self.spanner_2d_length
        unit = self.music_font.unit
        max_length_considered = unit(10)
        min_length_considered = unit(4)
        max_height = unit(2)
        min_height = unit(0.75)
        if length > max_length_considered:
            return max_height
        if length < min_length_considered:
            return min_height
        return interpolate(
            Point(min_length_considered, min_height),
            Point(max_length_considered, max_height),
            length,
        )

    def _derive_arch_length(self):
        spanner_length = self.spanner_2d_length
        unit = self.music_font.unit
        max_spanner_length_considered = unit(10)
        min_spanner_length_considered = unit(4)
        max_arch_length = unit(1)
        min_arch_length = unit(0)
        if spanner_length > max_spanner_length_considered:
            return max_arch_length
        if spanner_length < min_spanner_length_considered:
            return min_arch_length
        return interpolate(
            Point(min_spanner_length_considered, min_arch_length),
            Point(max_spanner_length_considered, max_arch_length),
            spanner_length,
        )

    def _draw_path(self):
        # Work out parameters
        abs_height = self.height if self.height else self._derive_height()
        arch_length = (
            self.arch_length if self.arch_length else self._derive_arch_length()
        )
        mid_height = abs_height * self.direction.value
        mid_upper_height = mid_height + (self.midpoint_thickness * self.direction.value)
        end_height = self.endpoint_thickness * self.direction.value
        # Draw upper curve part
        self.move_to(ZERO, end_height, self)
        control_1 = Point(arch_length, mid_upper_height)
        control_1_parent = self
        control_2 = Point(
            self.end_pos.x - arch_length, self.end_pos.y + mid_upper_height
        )
        control_2_parent = self.end_parent
        end = Point(self.end_pos.x, self.end_pos.y + end_height)
        end_parent = self.end_parent
        self.cubic_to(
            control_1.x,
            control_1.y,
            control_2.x,
            control_2.y,
            end.x,
            end.y,
            control_1_parent,
            control_2_parent,
            end_parent,
        )
        # Draw right-side end
        self.line_to(self.end_pos.x, self.end_pos.y, self.end_parent)
        # Draw lower curve part
        control_1 = Point(self.end_pos.x - arch_length, self.end_pos.y + mid_height)
        control_1_parent = self.end_parent
        control_2 = Point(arch_length, mid_height)
        control_2_parent = self
        end = ORIGIN
        end_parent = self
        self.cubic_to(
            control_1.x,
            control_1.y,
            control_2.x,
            control_2.y,
            end.x,
            end.y,
            control_1_parent,
            control_2_parent,
            end_parent,
        )
