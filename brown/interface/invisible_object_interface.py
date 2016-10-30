from PyQt5 import QtWidgets

from brown.interface.graphic_object_interface import GraphicObjectInterface


class InvisibleObjectInterface(GraphicObjectInterface):
    """
    Interface for a non-drawing object with a position, parent, and children.
    """
    def __init__(self, x, y, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the parent.
            y (float): The y position of the path relative to the parent.
            parent (GraphicObjectInterface): The parent of the object
        """
        # TODO: Is there a better way to model an invisible object?
        self._qt_object = QtWidgets.QGraphicsRectItem(x, y, 100, 100)
        self._qt_object.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents)
        self.x = x
        self.y = y
        self.parent = parent
