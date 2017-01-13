from brown.core.path import Path
from brown.primitives.staff_object import StaffObject
from brown.utils.point import Point
from brown.utils.units import Mm
from brown.core.pen import Pen
from brown.core.brush import Brush


class Beam(Path, StaffObject):

    def __init__(self, start, stop):
        """
        Args:
            start (AnchoredPoint): The starting (left) position of the beam
            stop (AnchoredPoint): The ending (right) position of the beam

        TODO: This init pattern of AnchoredPoints may not be the most elegant
              way to handle beams. They probably shouldn't be considered
              spanners because partial beamlets (ie dotted 8th + 16th)
              will probably be anchored at start and stop to the same
              chordrest. When implementing auto beaming, stay open to
              reworking this class's logic.
        """
        pen = Pen((0, 0, 0, 0))
        brush = Brush((0, 0, 0, 255))
        Path.__init__(self,
                      Point(Mm(0), Mm(0)),
                      pen=pen,
                      brush=brush,
                      parent=start.parent)
        StaffObject.__init__(self, start.parent)
        self.beam_thickness = self.staff.music_font.engraving_defaults['beamThickness']
        # Draw beam
        self.line_to(stop)
        self.line_to(stop.x, stop.y + self.beam_thickness, stop.parent)
        self.line_to(start.x, start.y + self.beam_thickness, start.parent)
        self.close_subpath()
