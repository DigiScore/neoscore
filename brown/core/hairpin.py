import math

from brown.core.graphic_object import GraphicObject
from brown.core.path import Path
from brown.core.spanner import Spanner
from brown.core.staff_object import StaffObject
from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point
from brown.utils.units import Unit


class Hairpin(Path, StaffObject, Spanner):

    """A crescendo/diminuendo hairpin spanner."""

    def __init__(self, start, stop, direction, width=None):
        """
        Args:
            start (ParentPoint or tuple init args): The starting point.
                This must have a parent which is a StaffObject or Staff.
            stop (ParentPoint or tuple init args): The stopping point.
                If this point's parent is `None`, the parent will default
                to the starting point.
            direction (int): The direction of the hairpin,
                where `-1` means diminuendo (>)
                and `1` means crescendo (<).
            width (Unit): The width of the wide hairpin part.
                Defaults to `self.staff.unit(1)`
        """
        start = (start if isinstance(start, ParentPoint)
                 else ParentPoint(*start))
        stop = (stop if isinstance(stop, ParentPoint)
                else ParentPoint(*stop))
        Path.__init__(self,
                      start,
                      parent=start.parent)
        StaffObject.__init__(self, start.parent)
        Spanner.__init__(self, stop, stop.parent)
        self.direction = direction
        self.width = width if width is not None else self.staff.unit(1)
        self.thickness = self.staff.music_font.engraving_defaults[
            'hairpinThickness']
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
            raise ValueError('Hairpin.direction must be -1 or 1')
        else:
            self._direction = value

    ######## PRIVATE METHODS ########

    def _find_hairpin_points(self):
        """Find the hairpin path points for a set of parameters.

        Returns:
            tuple(ParentPoint, ParentPoint, ParentPoint):
                The three points of the path. The center point
                is the point on the small end of the hairpin,
                while the outer points are those on the open
                end of the shape.
        """
        if self.direction == -1:
            joint = ParentPoint(
                self.end_pos.x, self.end_pos.y, parent=self.end_parent)
            end_center = ParentPoint(
                self.x, self.y, parent=self.parent)
        else:
            joint = ParentPoint(
                self.x, self.y, parent=self.parent)
            end_center = ParentPoint(
                self.end_pos.x, self.end_pos.y, parent=self.end_parent)
        dist = self.width / 2
        # Find relative distance from joint to end_center
        parent_distance = GraphicObject.map_between_items(
            joint.parent, end_center.parent)
        relative_stop = (parent_distance
                         + Point(end_center.x, end_center.y)
                         - Point(joint.x, joint.y))
        if relative_stop.y == Unit(0):
            return(
                (ParentPoint(end_center.x,
                               end_center.y + dist,
                               parent=end_center.parent)),
                joint,
                (ParentPoint(end_center.x,
                               end_center.y - dist,
                               parent=end_center.parent))
            )
        elif relative_stop.x == Unit(0):
            return(
                (ParentPoint(end_center.x + dist,
                               end_center.y,
                               parent=end_center.parent)),
                joint,
                (ParentPoint(end_center.x - dist,
                               end_center.y,
                               parent=end_center.parent))
            )
        # else ...

        # Find the two points (self.width / 2) away from the end_center
        # which lie on the line perpendicular to the spanner line.

        #   Note that there is no risk of division by zero because
        #   previous if / elif statements catch those possibilities
        center_slope = relative_stop.y / relative_stop.x
        opening_slope = (center_slope * -1) ** -1
        opening_y_intercept = (opening_slope * end_center.x) - end_center.y
        # Find needed x coordinates of outer points
        #     x = dist / sqrt(1 + slope^2)
        first_x = end_center.x + (dist / math.sqrt(type(opening_slope)(1)
                                                   + (opening_slope ** 2)))
        last_x = end_center.x - (dist / math.sqrt(type(opening_slope)(1)
                                                  + (opening_slope ** 2)))
        # Calculate matching y coordinates from opening line function
        first_y = (opening_slope * first_x) - opening_y_intercept
        last_y = (opening_slope * last_x) - opening_y_intercept
        return(
                (ParentPoint(first_x, first_y, parent=end_center.parent)),
                joint,
                (ParentPoint(last_x, last_y, parent=end_center.parent))
        )

    def _draw_path(self):
        """Draw the hairpin shape.

        Returns: None
        """
        first, mid, last = self._find_hairpin_points()
        self.move_to(first.x, first.y, first.parent)
        self.line_to(mid.x, mid.y, mid.parent)
        self.line_to(last.x, last.y, last.parent)
