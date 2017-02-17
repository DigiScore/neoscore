from PyQt5 import QtWidgets

from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.utils.point import Point
from brown.utils.units import Unit


"""A mock concrete GraphicObjectInterface subclass for testing"""


class MockGraphicObjectInterface(GraphicObjectInterface):

    """Only need to implement init for a functional mock subclass"""

    def __init__(self, pos, pen=None, brush=None):
        self._qt_object = QtWidgets.QGraphicsRectItem(
            0, 0, 10, 10)
        self.pos = pos
        self.pen = pen
        self.brush = brush
