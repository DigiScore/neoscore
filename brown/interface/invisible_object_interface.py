from PyQt5 import QtWidgets

from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.utils.unit import Unit
from brown.utils.point import Point


class InvisibleObjectInterface(GraphicObjectInterface):
    """
    Interface for a non-drawing object with a position, parent, and children.
    """
    def __init__(self, pos, parent=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the object
                relative to the document.
            parent (GraphicObjectInterface): The parent of the object
        """
        # TODO: Is there a better way to model an invisible object?
        pos_point = Point.with_unit(pos, unit=Unit)
        self._qt_object = QtWidgets.QGraphicsRectItem(
            pos_point.x.value, pos_point.y.value, 1, 1)
        self._qt_object.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents)
        self.pos = pos_point
        self.parent = parent
