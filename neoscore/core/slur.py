from typing import Optional

from neoscore.core.brush import Brush
from neoscore.core.graphic_object import GraphicObject
from neoscore.core.path import Path
from neoscore.core.spanner_2d import Spanner2D
from neoscore.core.staff_object import StaffObject
from neoscore.models.vertical_direction import VerticalDirection
from neoscore.utils.point import Point, PointDef


class Slur(Path, StaffObject, Spanner2D):

    """A slur spanning between two StaffObjects.

    By default, the parent will be the starting object.
    """

    def __init__(
        self,
        start: PointDef,
        start_parent: GraphicObject,
        stop: PointDef,
        stop_parent: Optional[GraphicObject],
        direction: VerticalDirection = VerticalDirection.UP,
    ):
        """
        Args:
            start: The starting point.
            start_parent: The parent for the starting position.
                Must be a staff or in one.
            stop: The stopping point.
            stop_parent: The parent for the ending position.
                If `None`, defaults to `self`.
            direction: The vertical direction the slur arches.
        """
        Path.__init__(self, start, parent=start_parent, brush=Brush((0, 0, 0, 255)))
        StaffObject.__init__(self, self.parent)
        stop = Point.from_def(stop)
        Spanner2D.__init__(self, stop, stop_parent or self)
        self.direction = direction
        # Load relevant engraving defaults from music font
        engraving_defaults = self.staff.music_font.engraving_defaults
        self.midpoint_thickness = self.staff.unit(
            engraving_defaults["slurMidpointThickness"]
        )
        self.endpoint_thickness = self.staff.unit(
            engraving_defaults["slurEndpointThickness"]
        )
        self._draw_path()

    ######## PRIVATE METHODS ########

    def _draw_path(self):
        mid_height = self.staff.unit(2) * self.direction.value
        mid_upper_height = (
            self.staff.unit(2) + self.midpoint_thickness
        ) * self.direction.value
        end_height = self.endpoint_thickness * self.direction.value
        # Draw upper curve part
        self.move_to(self.staff.unit(0), end_height, self)
        control_1 = Point(self.staff.unit(1), mid_upper_height)
        control_1_parent = self
        control_2 = Point(
            self.end_pos.x - self.staff.unit(1), self.end_pos.y + mid_upper_height
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
            self.end_pos.x - self.staff.unit(1), self.end_pos.y + mid_height
        )
        control_1_parent = self.end_parent
        control_2 = Point(self.x + self.staff.unit(1), self.y + mid_height)
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
