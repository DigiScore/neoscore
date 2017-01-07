from brown.core.path import Path
from brown.core.path_element import PathElement
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

    def __init__(self, start_object, stop_object, direction=-1):
        """
        Args:
            start_object (StaffObject):
            stop_object (StaffObject):
            direction (int): The direction of the slur, where
                -1 indicates curving upward, and 1 vice versa.
        """
        # TODO: Support path element offsets
        Path.__init__(self, (Unit(0), Unit(0)),
                      parent=start_object,
                      brush=Brush((0, 0, 0, 255)))
        StaffObject.__init__(self, start_object)
        Spanner.__init__(self, start_object, stop_object)
        self.pos = Point(self.staff.unit(0), self.staff.unit(0))
        self.direction = direction
        # Load relevant engraving defaults from music font
        engraving_defaults = self.staff.default_music_font.engraving_defaults
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
        self.move_to(AnchoredPoint(self.staff.unit(0),
                                   end_height,
                                   self.start))
        control_1 = AnchoredPoint(self.staff.unit(1),
                                  mid_upper_height,
                                  self.start)
        control_2 = AnchoredPoint(self.staff.unit(-1),
                                  mid_upper_height,
                                  self.stop)
        end = AnchoredPoint(self.staff.unit(0),
                            end_height,
                            self.stop)
        self.cubic_to(control_1, control_2, end)
        # Draw right-side end
        self.line_to(AnchoredPoint(self.staff.unit(0),
                                   self.staff.unit(0),
                                   self.stop))
        # Draw lower curve part
        control_1 = AnchoredPoint(self.staff.unit(-1),
                                  mid_height,
                                  self.stop)
        control_2 = AnchoredPoint(self.staff.unit(1),
                                  mid_height,
                                  self.start)
        end = AnchoredPoint(self.staff.unit(0),
                            self.staff.unit(0),
                            self.start)
        self.cubic_to(control_1, control_2, end)
        self.close_subpath()
