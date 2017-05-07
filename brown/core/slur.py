from brown.core.brush import Brush
from brown.core.path import Path
from brown.core.spanner import Spanner
from brown.core.staff_object import StaffObject
from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point


class Slur(Path, StaffObject, Spanner):

    """A slur spanning between two StaffObjects.

    By default, the parent will be the starting object.
    """

    def __init__(self, start, stop, direction=-1):
        """
        Args:
            start (ParentPoint or tuple init args):
            stop (ParentPoint or tuple init args):
            direction (int): The direction of the slur, where
                `-1` indicates curving upward, and `1` vice versa.
        """
        start = (start if isinstance(start, ParentPoint)
                 else ParentPoint(*start))
        stop = (stop if isinstance(stop, ParentPoint)
                else ParentPoint(*stop))
        Path.__init__(self, (start.x, start.y),
                      parent=start.parent,
                      brush=Brush((0, 0, 0, 255)))
        StaffObject.__init__(self, self.parent)
        Spanner.__init__(self, Point(stop.x, stop.y), stop.parent)
        self.direction = direction
        # Load relevant engraving defaults from music font
        engraving_defaults = self.staff.music_font.engraving_defaults
        self.midpoint_thickness = self.staff.unit(
            engraving_defaults['slurMidpointThickness'])
        self.endpoint_thickness = self.staff.unit(
            engraving_defaults['slurEndpointThickness'])
        self._draw_path()

    ######## PRIVATE METHODS ########

    def _draw_path(self):
        """Draw the slur shape.

        Returns: None
        """
        mid_height = self.staff.unit(2) * self.direction
        mid_upper_height = ((self.staff.unit(2) + self.midpoint_thickness)
                            * self.direction)
        end_height = self.endpoint_thickness * self.direction
        # Draw upper curve part
        self.move_to(self.staff.unit(0),
                     end_height,
                     self)
        control_1 = ParentPoint(self.staff.unit(1),
                                mid_upper_height,
                                parent=self)
        control_2 = ParentPoint(self.end_pos.x - self.staff.unit(1),
                                self.end_pos.y + mid_upper_height,
                                parent=self.end_parent)
        end = ParentPoint(self.end_pos.x,
                          self.end_pos.y + end_height,
                          parent=self.end_parent)
        self.cubic_to(control_1.x, control_1.y,
                      control_2.x, control_2.y,
                      end.x, end.y,
                      control_1.parent, control_2.parent, end.parent)
        # Draw right-side end
        self.line_to(self.end_pos.x,
                     self.end_pos.y,
                     self.end_parent)
        # Draw lower curve part
        control_1 = ParentPoint(self.end_pos.x - self.staff.unit(1),
                                self.end_pos.y + mid_height,
                                parent=self.end_parent)
        control_2 = ParentPoint(self.x + self.staff.unit(1),
                                self.y + mid_height,
                                parent=self)
        end = ParentPoint(self.x,
                          self.y,
                          parent=self)
        self.cubic_to(control_1.x, control_1.y,
                      control_2.x, control_2.y,
                      end.x, end.y,
                      control_1.parent, control_2.parent, end.parent)
        self.close_subpath()
