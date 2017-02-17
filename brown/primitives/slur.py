from brown.core.path import Path
from brown.primitives.staff_object import StaffObject
from brown.primitives.spanner import Spanner
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.point import Point
from brown.utils.units import Unit
from brown.core.brush import Brush


class Slur(Path, StaffObject, Spanner):

    """A slur spanning between two StaffObjects.

    By default, the parent will be the starting object.
    """

    def __init__(self, start, stop, direction=-1):
        """
        Args:
            start (AnchoredPoint or tuple init args):
            stop (AnchoredPoint or tuple init args):
            direction (int): The direction of the slur, where
                -1 indicates curving upward, and 1 vice versa.
        """
        Spanner.__init__(self, start, stop)
        Path.__init__(self, (Unit(0), Unit(0)),
                      parent=self.start.parent,
                      brush=Brush((0, 0, 0, 255)))
        StaffObject.__init__(self, self.parent)
        # Is this pos override necessary? Probably not???
        self.pos = Point(self.staff.unit(0), self.staff.unit(0))
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
        mid_upper_height = ((self.staff.unit(2) + self.midpoint_thickness) *
                            self.direction)
        end_height = (self.endpoint_thickness) * self.direction
        # Draw upper curve part
        self.move_to(self.staff.unit(0),
                     end_height,
                     self.start.parent)
        control_1 = AnchoredPoint(self.staff.unit(1),
                                  mid_upper_height,
                                  self.start.parent)
        control_2 = AnchoredPoint(self.staff.unit(-1),
                                  mid_upper_height,
                                  self.stop.parent)
        end = AnchoredPoint(self.staff.unit(0),
                            end_height,
                            self.stop.parent)
        self.cubic_to(control_1, control_2, end)
        # Draw right-side end
        self.line_to(self.staff.unit(0),
                     self.staff.unit(0),
                     self.stop.parent)
        # Draw lower curve part
        control_1 = AnchoredPoint(self.staff.unit(-1),
                                  mid_height,
                                  self.stop.parent)
        control_2 = AnchoredPoint(self.staff.unit(1),
                                  mid_height,
                                  self.start.parent)
        end = AnchoredPoint(self.staff.unit(0),
                            self.staff.unit(0),
                            self.start.parent)
        self.cubic_to(control_1, control_2, end)
        self.close_subpath()
