from brown.core.path import Path
from brown.core.path_element import PathElement
from brown.primitives.staff_object import StaffObject
from brown.primitives.spanner import Spanner
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.point import Point
from brown.utils.units import Unit


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
        # TODO: Support direction flipping
        Path.__init__(self, (Unit(0), Unit(0)), parent=start_object)
        StaffObject.__init__(self, start_object)
        Spanner.__init__(self, start_object, stop_object)
        self.pos = Point(self.staff.unit(0), self.staff.unit(0))
        self.direction = direction
        self._draw_path()

    ######## PRIVATE METHODS ########

    def _draw_path(self):
        """Draw the slur shape.

        Returns: None
        """
        control_1 = AnchoredPoint(self.staff.unit(1),
                                  self.staff.unit(-3),
                                  self.start)
        control_2 = AnchoredPoint(self.staff.unit(-1),
                                  self.staff.unit(-3),
                                  self.stop)
        end = AnchoredPoint(self.staff.unit(0),
                            self.staff.unit(0),
                            self.stop)
        self.cubic_to(control_1, control_2, end)
