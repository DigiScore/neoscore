import math

from examples.feldman_projection_2.grid_unit import GridUnit
from examples.feldman_projection_2.measure import Measure
from neoscore.core.brush import Brush
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Unit


class Event(PositionedObject):
    """A graphical event wrapped in a box

    This plain class can notate plain empty rectangle events, but it can be subclassed
    to create boxes with text and glyphs inside them.
    """

    box_pen = Pen(thickness=GridUnit(0.07))

    def __init__(self, pos: PointDef, parent: PositionedObject, length: Unit):
        PositionedObject.__init__(self, pos, parent)
        self.path = Path.rect(
            ORIGIN,
            self,
            length,
            GridUnit(1),
            Brush.no_brush(),
            Event.box_pen,
        )

    @staticmethod
    def lies_at_measure_boundary(pos_x: Unit) -> bool:
        remainder = pos_x.base_value % Measure(1).base_value
        print(remainder)
        tolerance = 0.5
        return math.isclose(remainder, 0, abs_tol=tolerance) or math.isclose(
            remainder, 1, abs_tol=tolerance
        )
