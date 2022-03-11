from neoscore.core.brush_pattern import BrushPattern
from neoscore.core.pen_cap_style import PenCapStyle
from neoscore.core.pen_join_style import PenJoinStyle
from neoscore.core.pen_pattern import PenPattern
from neoscore.interface.brush_interface import BrushInterface
from neoscore.interface.graphic_object_interface import GraphicObjectInterface
from neoscore.interface.pen_interface import PenInterface
from neoscore.utils.color import Color
from neoscore.utils.units import GraphicUnit

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
