from PyQt5 import QtWidgets

from brown.utils.brush_pattern import BrushPattern
from brown.utils.pen_pattern import PenPattern
from brown.interface.brush_interface import BrushInterface
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.pen_interface import PenInterface
from brown.utils.color import Color


"""A mock concrete GraphicObjectInterface subclass for testing"""


class MockGraphicObjectInterface(GraphicObjectInterface):

    """Only need to implement init for a functional mock subclass"""

    def __init__(self, pos, pen=None, brush=None):
        self.qt_object = QtWidgets.QGraphicsRectItem(
            0, 0, 10, 10)
        self.pos = pos
        if pen:
            self.pen = pen
        else:
            self.pen = PenInterface(
                Color('#000000'), 0, PenPattern.SOLID)
        if brush:
            self.brush = brush
        else:
            self.brush = BrushInterface(
                Color('#000000'), BrushPattern.SOLID)
