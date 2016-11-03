from PyQt5 import QtWidgets

from brown.interface.graphic_object_interface import GraphicObjectInterface


"""

A mock concrete GraphicObjectInterface subclass for testing

"""


class MockGraphicObject(GraphicObjectInterface):

    """Only need to implement init for a functional mock subclass"""

    def __init__(self, parent, x, y, pen=None, brush=None):
        self._qt_object = QtWidgets.QGraphicsRectItem(x, y, 10, 10)
        self.x = x
        self.y = y
        self.parent = parent
        self.pen = pen
        self.brush = brush

    # TODO: implement render() for testing once render testing is figured out
