from brown.primitives.multi_staff_object import MultiStaffObject
from brown.utils.units import Unit
from brown.core.path import Path
from brown.core.pen import Pen
from brown.core.graphic_object import GraphicObject


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
            position_x (StaffUnit): The barline position relative to
                the top staff.
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
        offset = GraphicObject.map_between_items(self.lowest_staff,
                                                 self.highest_staff)
        bottom_x = position_x + offset.x
        self.line_to(bottom_x,
                     self.lowest_staff.height,
                     parent=self.lowest_staff)
