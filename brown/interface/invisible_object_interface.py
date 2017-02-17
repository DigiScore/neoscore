from PyQt5 import QtWidgets, QtCore

from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.core import brown
from brown.utils.units import GraphicUnit
from brown.utils.point import Point
from brown.interface.qt_to_util import point_to_qt_point_f


class InvisibleObjectInterface(GraphicObjectInterface):

    """An invisible object.

    This is implemented as a square with size 1.
    When passed to the graphics engine, it is flagged to not be rendered.

    A future, more elegant, implementation might consider an invisible object
    as a single point, which may or may not ever be passed to the
    graphics engine.
    """

    def __init__(self, pos):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the object
                relative to the document.
        """
        q_rect = QtCore.QRectF(0, 0, 1, 1)
        self._qt_object = QtWidgets.QGraphicsRectItem(q_rect)
        self._qt_object.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents)
        # Let pos setter set _qt_object position
        self.pos = Point.with_unit(pos, unit=GraphicUnit)

    def render(self):
        brown._app_interface.scene.addItem(self._qt_object)
