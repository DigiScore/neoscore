from brown.primitives.multi_staff_object import MultiStaffObject
from brown.utils.units import Unit
from brown.core.path import Path
from brown.utils.anchored_point import AnchoredPoint
from brown.core.pen import Pen


class BarLine(Path, MultiStaffObject):

    """A single bar line.

    This is drawn as a single vertical line at a given x coordinate
    spanning the full height of a series of staves.

    The thickness of the line is determined by the engraving defaults
    on the top staff.
    """

    def __init__(self, position_x, staves):
        """
        Args
            position_x (StaffUnit):
            staves (iter[Staff]):
        """
        MultiStaffObject.__init__(self, set(staves))
        Path.__init__(self,
                      (position_x, Unit(0)),
                      parent=self.highest_staff)
        engraving_defaults = self.highest_staff.music_font.engraving_defaults
        thickness = engraving_defaults['thinBarlineThickness']
        self.pen = Pen(thickness=thickness)
        # Draw path
        # NOTE: This assumes that all staves begin at the same x position.
        #       The line will be skewed otherwise.
        self.line_to(position_x,
                     self.lowest_staff.height,
                     self.lowest_staff)
