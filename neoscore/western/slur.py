from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core.brush import SimpleBrushDef
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import SimplePenDef
from neoscore.core.spanner_2d import Spanner2D
from neoscore.models.directions import VerticalDirection
from neoscore.utils.point import Point, PointDef

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Slur(MusicPath, Spanner2D):

    """A slur, also usable as a tie.

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Parent,
        end_pos: PointDef,
        end_parent: Optional[Parent],
        direction: VerticalDirection = VerticalDirection.UP,
        font: Optional[MusicFont] = None,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """
        Args:
            pos: The starting point.
            parent: The parent for the starting position. If no font is given,
                this or one of its ancestors must implement `HasMusicFont`.
            end_pos: The stopping point.
            end_parent: The parent for the ending position.
                If `None`, defaults to `self`.
            direction: The vertical direction the slur arches.
            font: If provided, this overrides any font found in the ancestor chain.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        MusicPath.__init__(self, pos, parent, font, brush, pen)
        end_pos = Point.from_def(end_pos)
        Spanner2D.__init__(self, end_pos, end_parent or self)
        self.direction = direction
        # Load relevant engraving defaults from music font
        self.midpoint_thickness = self.music_font.engraving_defaults[
            "slurMidpointThickness"
        ]
        self.endpoint_thickness = self.music_font.engraving_defaults[
            "slurEndpointThickness"
        ]
        self._draw_path()

    ######## PRIVATE METHODS ########

    def _draw_path(self):
        mid_height = self.music_font.unit(2) * self.direction.value
        mid_upper_height = (
            self.music_font.unit(2) + self.midpoint_thickness
        ) * self.direction.value
        end_height = self.endpoint_thickness * self.direction.value
        # Draw upper curve part
        self.move_to(self.music_font.unit(0), end_height, self)
        control_1 = Point(self.music_font.unit(1), mid_upper_height)
        control_1_parent = self
        control_2 = Point(
            self.end_pos.x - self.music_font.unit(1), self.end_pos.y + mid_upper_height
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
        control_1 = Point(
            self.end_pos.x - self.music_font.unit(1), self.end_pos.y + mid_height
        )
        control_1_parent = self.end_parent
        control_2 = Point(self.x + self.music_font.unit(1), self.y + mid_height)
        control_2_parent = self
        end = Point(self.x, self.y)
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
        self.close_subpath()
