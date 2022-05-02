from examples.feldman_projections_2.grid_unit import GridUnit
from neoscore.core.brush import Brush
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Unit


class Event(PositionedObject):
    """A boxed event."""

    box_pen = Pen(thickness=GridUnit(0.07), join_style=PenJoinStyle.MITER)

    def __init__(self, pos: Point, parent: PositionedObject, length: Unit):
        PositionedObject.__init__(self, pos, parent)
        self.path = Path.rect(
            pos, parent, length, GridUnit(1), Brush.no_brush(), Event.box_pen
        )
