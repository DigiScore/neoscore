from __future__ import annotations

import math
from typing import Optional

from neoscore.core.brush import Brush
from neoscore.core.directions import DirectionX
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.units import ZERO, Unit


class Hairpin(Spanner2D, MusicPath):

    """A crescendo/diminuendo hairpin spanner.

    While this is a path, it requires a music font from which to
    derive its appearance.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: PositionedObject,
        end_pos: PointDef,
        end_parent: Optional[PositionedObject] = None,
        direction: DirectionX = DirectionX.RIGHT,
        width: Optional[Unit] = None,
        font: Optional[MusicFont] = None,
    ):
        """
        Args:
            pos: The starting point.
            parent: The parent for the starting position. If no font is given,
                this or one of its ancestors must implement :obj:`.HasMusicFont`.
            end_pos: The stopping point.
            end_parent: The parent for the ending position.
                If ``None``, defaults to ``self``.
            direction: The direction of the hairpin, where ``LEFT`` means diminuendo (>)
                and ``RIGHT`` means crescendo (<).
            width: The width of the wide hairpin. Defaults to 1 staff unit.
            font: If provided, this overrides any font found in the ancestor chain.
        """
        MusicPath.__init__(self, pos, parent, font=font, brush=Brush.no_brush())
        end_pos = Point.from_def(end_pos)
        Spanner2D.__init__(self, end_pos, end_parent or self)
        self.direction = direction
        self.width = width if width is not None else self.music_font.unit(1)
        self.pen = Pen(thickness=self.music_font.engraving_defaults["hairpinThickness"])
        self._draw_path()

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    @property
    def direction(self) -> DirectionX:
        """The direction of the hairpin.

        ``LEFT`` means diminuendo (>) and ``RIGHT`` means crescendo (<).
        """
        return self._direction

    @direction.setter
    def direction(self, value: DirectionX):
        self._direction = value

    def _find_hairpin_points(
        self,
    ) -> Tuple[
        Point, PositionedObject, Point, PositionedObject, Point, PositionedObject
    ]:
        """Find the hairpin path points for a set of parameters.

        The returned tuple is 3 pairs of Points and parents, where the
        outer 2 represent the wide ends of the hairpin and the middle
        represents the small end joint.
        """
        if self.direction == DirectionX.LEFT:
            joint_pos = self.end_pos
            joint_parent = self.end_parent
            end_center_pos = self.pos
            end_center_parent = self.parent
        else:
            joint_pos = self.pos
            joint_parent = self.parent
            end_center_pos = self.end_pos
            end_center_parent = self.end_parent
        dist = self.width / 2
        # Find relative distance from joint to end_center_pos
        parent_distance = joint_parent.map_to(end_center_parent)
        relative_stop = parent_distance + end_center_pos - joint_pos
        if relative_stop.y == ZERO:
            return (
                Point(end_center_pos.x, end_center_pos.y + dist),
                end_center_parent,
                joint_pos,
                joint_parent,
                Point(end_center_pos.x, end_center_pos.y - dist),
                end_center_parent,
            )
        elif relative_stop.x == ZERO:
            return (
                Point(end_center_pos.x + dist, end_center_pos.y),
                end_center_parent,
                joint_pos,
                joint_parent,
                Point(end_center_pos.x - dist, end_center_pos.y),
                end_center_parent,
            )
        # else ...

        # Find the two points (self.width / 2) away from the end_center_pos
        # which lie on the line perpendicular to the spanner line.

        #   Note that there is no risk of division by zero because
        #   previous if / elif statements catch those possibilities
        center_slope = relative_stop.y / relative_stop.x
        opening_slope = (center_slope * -1) ** -1
        opening_y_intercept = (end_center_pos.x * opening_slope) - end_center_pos.y
        # Find needed x coordinates of outer points
        #     x = dist / sqrt(1 + slope^2)
        first_x = end_center_pos.x + (dist / math.sqrt(1 + (opening_slope**2)))
        last_x = end_center_pos.x - (dist / math.sqrt(1 + (opening_slope**2)))
        # Calculate matching y coordinates from opening line function
        first_y = (first_x * opening_slope) - opening_y_intercept
        last_y = (last_x * opening_slope) - opening_y_intercept
        return (
            Point(first_x, first_y),
            end_center_parent,
            joint_pos,
            joint_parent,
            Point(last_x, last_y),
            end_center_parent,
        )

    def _draw_path(self):
        (
            first_pos,
            first_parent,
            mid_pos,
            mid_parent,
            last_pos,
            last_parent,
        ) = self._find_hairpin_points()
        self.move_to(first_pos.x, first_pos.y, first_parent)
        self.line_to(mid_pos.x, mid_pos.y, mid_parent)
        self.line_to(last_pos.x, last_pos.y, last_parent)
