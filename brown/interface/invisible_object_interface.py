from PyQt5 import QtWidgets

from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.core import brown
from brown.utils.units import Unit
from brown.utils.point import Point


class InvisibleObjectInterface(GraphicObjectInterface):
    """Interface for a non-drawing object with a position."""
    def __init__(self, pos):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the object
                relative to the document.
        """
        # TODO: Is there a better way to model an invisible object?
        pos_point = Point.with_unit(pos, unit=Unit)
        self._qt_object = QtWidgets.QGraphicsRectItem(
            pos_point.x.value, pos_point.y.value, 1, 1)
        self._qt_object.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents)
        self.pos = pos_point

    def render(self):
        brown._app_interface.scene.addItem(self._qt_object)
