from neoscore.core.graphic_object import GraphicObject
from neoscore.core.path import Path
from neoscore.core.staff_object import StaffObject
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import ZERO


class Beam(Path, StaffObject):

    """A rhythmic beam connecting groups of notes.

    This is a single beam - for multiple layers of beams
    (e.g. 2 for 16th notes), multiple `Beam`s must be stacked
    on top of each other.
    """

    def __init__(
        self,
        start: PointDef,
        start_parent: GraphicObject,
        stop: PointDef,
        stop_parent: GraphicObject,
    ):
        """
        Args:
            start: The starting (left) position of the beam
            start_parent: The parent for the starting position.
                Must be a staff or in one.
            stop: The ending (right) position of the beam
            stop_parent: The parent for the ending position.
                Must be a staff or in one.
        """
        Path.__init__(self, start, parent=start_parent)
        StaffObject.__init__(self, start_parent)
        self.beam_thickness = self.staff.music_font.engraving_defaults["beamThickness"]
        # Draw beam
        stop = Point.from_def(stop)
        self.line_to(stop.x, stop.y, stop_parent)
        self.line_to(stop.x, stop.y + self.beam_thickness, stop_parent)
        self.line_to(ZERO, self.beam_thickness, self)
        self.close_subpath()
