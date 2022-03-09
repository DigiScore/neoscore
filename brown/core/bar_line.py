from collections.abc import Iterable
from brown.core.mapping import map_between
from brown.core.multi_staff_object import MultiStaffObject
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.staff import Staff
from brown.utils.point import Point
from brown.utils.units import ZERO, Unit


class BarLine(Path, MultiStaffObject):

    """A single bar line.

    This is drawn as a single vertical line at a given x coordinate
    spanning the full height of a series of staves.

    The thickness of the line is determined by the engraving defaults
    on the top staff.
    """

    def __init__(self, pos_x: Unit, staves: Iterable[Staff]):
        """
        Args:
            pos_x: The barline position relative to
                the top staff.
            staves:
        """
        MultiStaffObject.__init__(self, set(staves))
        Path.__init__(self, Point(pos_x, ZERO), parent=self.highest_staff)
        engraving_defaults = self.highest_staff.music_font.engraving_defaults
        thickness = engraving_defaults["thinBarlineThickness"]
        self.pen = Pen(thickness=thickness)
        # Draw path
        offset = map_between(self.lowest_staff, self.highest_staff)
        bottom_x = pos_x + offset.x
        self.line_to(bottom_x, self.lowest_staff.height, parent=self.lowest_staff)
