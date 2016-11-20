from PyQt5 import QtWidgets
from PyQt5 import QtGui

from brown.core import brown
from brown.utils.point import Point
from brown.utils.graphic_unit import GraphicUnit


class PathElementInterface:

    """An element of a path or subpath.

    Becuase QPainterPath::Element instances can't be directly created,
    to instantiate an instance of this class you should query the parent
    PathInterface.elements[-1] after creating an element, and pass its
    result to the constructor here.

    # TODO: Does this work?
    """

    def __init__(self, qt_object):
        """
        Args:
            qt_object (QPainterPath.Element)"""
        self._qt_object = qt_object
        self._pos = Point(GraphicUnit(qt_object.x), GraphicUnit(qt_object.y))

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._qt_object.x = float(value.x)
        self._qt_object.y = float(value.y)

    @property
    def is_curve_to(self):
        """bool: Whether this element is a curve-to element."""
        return self._qt_object.isCurveTo()

    @property
    def is_line_to(self):
        """bool: Whether this element is a line-to element."""
        return self._qt_object.isLineTo()

    @property
    def is_move_to(self):
        """bool: Whether this element is a move-to element."""
        return self._qt_object.isMoveTo()
