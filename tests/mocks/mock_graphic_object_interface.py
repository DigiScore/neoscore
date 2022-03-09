
from brown.core.brush_pattern import BrushPattern
from brown.core.pen_cap_style import PenCapStyle
from brown.core.pen_join_style import PenJoinStyle
from brown.core.pen_pattern import PenPattern
from brown.interface.brush_interface import BrushInterface
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color
from brown.utils.units import GraphicUnit

"""A mock concrete GraphicObjectInterface subclass for testing"""


class MockGraphicObjectInterface(GraphicObjectInterface):

    """Only need to implement init for a functional mock subclass"""

    def __init__(self, pos, pen=None, brush=None):
        super().__init__()
        self._pos = pos
        if pen:
            self._pen = pen
        else:
            self._pen = PenInterface(
                Color("#000000"),
                GraphicUnit(0),
                PenPattern.SOLID,
                PenJoinStyle.BEVEL,
                PenCapStyle.SQUARE,
            )
        if brush:
            self._brush = brush
        else:
            self._brush = BrushInterface(Color("#000000"), BrushPattern.SOLID)
