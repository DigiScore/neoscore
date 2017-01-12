from brown.primitives.staff_object import StaffObject
from brown.core.path import Path
from brown.utils.point import Point
from brown.core.pen import Pen


class BarLine(Path, StaffObject):

    """A single bar line.

    This is drawn as a single vertical line at a given x coordinate
    spanning the full height of a Staff.
    """

    def __init__(self, position_x, staff):
        """
        Args
            position_x (StaffUnit):
            staff (Staff):
        """

        Path.__init__(self, Point(position_x, staff.unit(0)), parent=staff)
        StaffObject.__init__(self, staff)
        thickness = (
            self.staff.music_font.engraving_defaults['thinBarlineThickness'])
        self.pen = Pen(thickness=thickness)
        # Draw path
        self.line_to(Point(self.staff.unit(0), self.staff.height))
