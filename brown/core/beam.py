from brown.core.path import Path
from brown.core.staff_object import StaffObject
from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class Beam(Path, StaffObject):

    """A rhythmic beam connecting groups of notes.

    This is a single beam - for multiple layers of beams
    (e.g. 2 for 16th notes), multiple `Beam`s must be stacked
    on top of each other.
    """

    def __init__(self, start, stop):
        """
        Args:
            start (ParentPoint or init tuple): The starting (left) position
                of the beam
            stop (ParentPoint or init tuple): The ending (right) position
                of the beam
        """
        if not isinstance(start, ParentPoint):
            start = ParentPoint(*start)
        if not isinstance(stop, ParentPoint):
            stop = ParentPoint(*stop)
        Path.__init__(self,
                      Point.from_parent_point(start),
                      parent=start.parent)
        StaffObject.__init__(self, start.parent)
        self.beam_thickness = self.staff.music_font.engraving_defaults[
            'beamThickness']
        # Draw beam
        self.line_to(stop.x, stop.y, stop.parent)
        self.line_to(stop.x, stop.y + self.beam_thickness, stop.parent)
        self.line_to(GraphicUnit(0), self.beam_thickness, self)
        self.close_subpath()
