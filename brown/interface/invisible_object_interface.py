from PyQt5 import QtWidgets

from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.core import brown
from brown.utils.units import Unit
from brown.utils.point import Point


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
        pos_point = Point.with_unit(pos, unit=Unit)
        self._qt_object = QtWidgets.QGraphicsRectItem(
            pos_point.x.value, pos_point.y.value, 1, 1)
        self._qt_object.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents)
        self.pos = pos_point

    def render(self):
        brown._app_interface.scene.addItem(self._qt_object)
