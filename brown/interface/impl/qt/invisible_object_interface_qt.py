from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.core import brown
from brown.interface.abstract.invisible_object_interface import InvisibleObjectInterface


class InvisibleObjectInterfaceQt(InvisibleObjectInterface):
    """
    Interface for a non-drawing object with a position, parent, and children.
    """
    def __init__(self, x, y):
        """
        Args:
            x (float): The x position of the path relative to the parent.
            y (float): The y position of the path relative to the parent.
        """
        # TODO: Is there a better way to model an invisible object?
        self._qt_object = QtWidgets.QGraphicsRectItem(x, y, 100, 100)
        self._qt_object.setFlag(QtWidgets.QGraphicsItem.ItemHasNoContents)
        self.x = x
        self.y = y

    ######## PUBLIC PROPERTIES ########

    @property
    def x(self):
        """
        float: The x position of the Path relative to the document
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._qt_object.setX(self._x)

    @property
    def y(self):
        """
        float: The y position of the Path relative to the document
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._qt_object.setY(self._y)

    @property
    def parent(self):
        """The interface of the parent object."""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        # HACK: Assumes the passed item has a _qt_object
        if value is not None:
            self._qt_object.setParentItem(value._qt_object)
        else:
            self._qt_object.setParentItem(None)
