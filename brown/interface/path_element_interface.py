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

    def __init__(self, qt_object, parent_path):
        """
        Args:
            qt_object (QPainterPath.Element)"""
        self._qt_object = qt_object
        self._parent_path = parent_path
        self._pos = Point.with_unit(qt_object.x, qt_object.y,
                                    unit_class=GraphicUnit)
        self._pos.on_change = self.parent_path._update_qt_object_path()

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._qt_object.x = float(value.x)
        self._qt_object.y = float(value.y)
        self.parent_path._update_qt_object_path()

    @property
    def parent_path(self):
        """PathInterface: The path this element belongs to.

        This property is read-only."""
        return self._parent_path

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
