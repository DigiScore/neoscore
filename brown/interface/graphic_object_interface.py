from PyQt5 import QtGui

from abc import ABC


class GraphicObjectInterface(ABC):
    """Interface for a generic graphic object.

    This is a top-level abstract interface class.
    """
    def __init__(self, x, y, pen=None, brush=None, parent=None):
        """
        Must define and set:

            self._qt_object = # Some subclass of QGraphicsItem
            self.x = x
            self.y = y
            self.parent = parent

        Args:
            x (float): The x position of the path relative to the document
            y (float): The y position of the path relative to the document
            pen (PenInterface): The pen to draw outlines with.
            brush (BrushInterface): The brush to draw outlines with.
        """
        raise NotImplementedError

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
    def pen(self):
        """
        PenInterface: The pen to draw outlines with
        """
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        if self._pen:
            self._qt_object.setPen(self._pen._qt_object)
        else:
            self._qt_object.setPen(QtGui.QPen())

    @property
    def brush(self):
        """
        BrushInterface: The brush to draw outlines with
        """
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        if self._brush:
            self._qt_object.setBrush(self._brush._qt_object)
        else:
            self._qt_object.setBrush(QtGui.QBrush())

    @property
    def parent(self):
        """The interface of the parent object."""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        if value is not None:
            self._qt_object.setParentItem(value._qt_object)
        else:
            self._qt_object.setParentItem(None)

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        raise NotImplementedError
