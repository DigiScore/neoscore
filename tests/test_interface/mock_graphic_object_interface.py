from PyQt5 import QtWidgets

from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.utils.point import Point
from brown.utils.units import Unit


"""A mock concrete GraphicObjectInterface subclass for testing"""


class MockGraphicObjectInterface(GraphicObjectInterface):

    """Only need to implement init for a functional mock subclass"""

    def __init__(self, pos, pen=None, brush=None, parent=None):
        pos_point = Point.with_unit(pos, unit=Unit)
        self._qt_object = QtWidgets.QGraphicsRectItem(
            pos_point.x.value, pos_point.y.value, 10, 10)
        self.pos = pos_point
        self.parent = parent
        self.pen = pen
        self.brush = brush

    # TODO: implement render() for testing once render testing is figured out
