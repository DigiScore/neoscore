import math
from typing import Optional

from neoscore.core.graphic_object import GraphicObject
from neoscore.core.mapping import map_between
from neoscore.core.path import Path
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.staff_object import StaffObject
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import ZERO, Unit


class Hairpin(Path, StaffObject, Spanner2D):

    """A crescendo/diminuendo hairpin spanner."""

    def __init__(
        self,
        start: PointDef,
        start_parent: GraphicObject,
        stop: PointDef,
        stop_parent: Optional[GraphicObject],
        direction: int,
        width: Optional[Unit] = None,
    ):
        """
        Args:
            start: The starting point.
            start_parent: The parent for the starting position.
                Must be a staff or in one.
            stop: The stopping point.
            stop_parent: The parent for the ending position.
                If `None`, defaults to `self`.
            direction: The direction of the hairpin, where `-1` means diminuendo (>)
                and `1` means crescendo (<).
            width: The width of the wide hairpin. Defaults to 1 staff unit.
        """
        Path.__init__(self, start, parent=start_parent)
        StaffObject.__init__(self, start_parent)
        stop = Point.from_def(stop)
        Spanner2D.__init__(self, stop, stop_parent or self)
        self.direction = direction
        self.width = width if width is not None else self.staff.unit(1)
        self.thickness = self.staff.music_font.engraving_defaults["hairpinThickness"]
        self._draw_path()

    ######## PUBLIC PROPERTIES ########

    @property
    def direction(self):
        """int: The direction of the hairpin.

        `-1` means diminuendo (>) and `1` means crescendo (<).
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        if value != 1 and value != -1:
            raise ValueError("Hairpin.direction must be -1 or 1")
        else:
            self._direction = value

    ######## PRIVATE METHODS ########

    def _find_hairpin_points(
        self,
    ) -> tuple[Point, GraphicObject, Point, GraphicObject, Point, GraphicObject]:
        """Find the hairpin path points for a set of parameters.

        The returned tuple is 3 pairs of Points and parents, where the
        outer 2 represent the wide ends of the hairpin and the middle
        represents the small end joint.
        """
        if self.direction == -1:
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
        parent_distance = map_between(joint_parent, end_center_parent)
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
        """Draw the hairpin shape.

        Returns: None
        """
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
