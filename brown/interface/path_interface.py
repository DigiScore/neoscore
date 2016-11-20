from PyQt5 import QtWidgets
from PyQt5 import QtGui

from brown.core import brown
from brown.utils.point import Point
from brown.utils.graphic_unit import GraphicUnit
from brown.interface.graphic_object_interface import GraphicObjectInterface
from brown.interface.path_element_interface import PathElementInterface


"""
Notes on Qt path quirks:
* At creation time, paths have an elementCount() of 0,
  but after a line is created, elementCount() == 2. First element
  is a moveTo to the origin; second is the lineTo you asked for
* If a lineTo is drawn to (0, 0), a moveTo 0, 0 is performed instead:

    line_to_origin = PathInterface((5, 6))
    line_to_origin.line_to((0, 0))
    assert(line_to_origin._qt_path == line_to_origin._qt_object.path())
    assert(line_to_origin._qt_path.elementCount() == 1)
    assert(line_to_origin._qt_path.elementAt(0).isMoveTo() == True)
    line_to_elsewhere = PathInterface((5, 6))
    line_to_elsewhere.line_to((1, 0))
    assert(line_to_elsewhere._qt_path == line_to_elsewhere._qt_object.path())
    assert(line_to_elsewhere._qt_path.elementCount() == 2)
    assert(line_to_elsewhere._qt_path.elementAt(0).isMoveTo() == True)
    assert(line_to_elsewhere._qt_path.elementAt(1).isLineTo() == True)
    # (All pass)

"""


class PathInterface(GraphicObjectInterface):
    """Interface for a generic graphic path object."""
    def __init__(self, pos, pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            pen (PenInterface): The pen to draw outlines with.
            brush (BrushInterface): The brush to draw outlines with.
            parent (GraphicObjectInterface):
        """
        self._qt_path = QtGui.QPainterPath()
        self._qt_object = QtWidgets.QGraphicsPathItem(self._qt_path)
        self.pos = pos
        self.pen = pen
        self.brush = brush
        self._current_path_position = Point(0, 0)
        self.parent = parent

    ######## PUBLIC PROPERTIES ########

    @property
    def current_path_position(self):
        """Point[GraphicUnit]: The current relative drawing position.

        This is the location from which operations like line_to() will draw,
        relative to the position of the Path (`self.x` and `self.y`).

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        if self.element_count:
            return self.element_at(-1).pos
        else:
            return Point(0, 0)

    @property
    def current_path_x(self):
        """GraphicUnit: The current relative drawing x-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self.current_path_position.x

    @property
    def current_path_y(self):
        """GraphicUnit: The current relative drawing y-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self.current_path_position.y

    @property
    def element_count(self):
        """int: The number of elements in the path."""
        return self._qt_path.elementCount()

    ######## Public Methods ########

    def line_to(self, pos):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `pos`, and move `self.current_path_position` to the new point.

        Args:
            pos (Point or tuple): The target position

        Returns: None
        """
        target = Point.with_unit(pos, unit_class=GraphicUnit)
        self._qt_path.lineTo(target.x.value, target.y.value)
        self._update_qt_object_path()

    def cubic_to(self,
                 control_1,
                 control_2,
                 end):
        """Draw a cubic spline from the current position to a new point.

        Moves `self.current_path_position` to the new end point.

        Args:
            control_1_x (Point): The local position of the 1st control point
            control_2_x (Point): The local position of the 2nd control point
            end_x (Point): The local position of the end point

        Returns: None
        """
        control_1_point = Point.with_unit(control_1, unit_class=GraphicUnit)
        control_2_point = Point.with_unit(control_2, unit_class=GraphicUnit)
        end_point = Point.with_unit(end, unit_class=GraphicUnit)
        self._qt_path.cubicTo(
            control_1_point.x.value,
            control_1_point.y.value,
            control_2_point.x.value,
            control_2_point.y.value,
            end_point.x.value,
            end_point.y.value)
        self._update_qt_object_path()

    def move_to(self, pos):
        """Close the current sub-path and start a new one.

        Args:
            pos (Point or tuple): The target position

        Returns: None
        """
        target = Point.with_unit(pos, unit_class=GraphicUnit)
        self._qt_path.moveTo(target.x.value, target.y.value)
        self._update_qt_object_path()

    def close_subpath(self):
        """Close the current sub-path and start a new one at (0, 0).

        This is equivalent to `move_to(0, 0)`

        Returns: None
        """
        self._qt_path.closeSubpath()
        self._update_qt_object_path()

    def element_at(self, index):
        """Find the element at a given index and return it.

        Args:
            index (int): The element index. Use -1 for the last index.

        Returns: PathElementInterface

        # TODO: Implement a list-like iterable wrapper around path elements?
        """
        if index < 0:
            qt_index = self.element_count + index
        else:
            qt_index = index
        return PathElementInterface(self._qt_path.elementAt(qt_index),
                                    self,
                                    qt_index)

    def set_element_position_at(self, index, pos):
        """Set the element at an index to a given position.

        Args:
            index (int): The element index to modify
            pos (Point[GraphicUnit] or tuple): The new position
                for the element.

        Returns: None
        """
        # TODO: Make index error guards when proper element list is made
        pos_x = float(pos[0])
        pos_y = float(pos[1])
        print('setting element at index {} to ({}, {})'.format(index, pos_x, pos_y))
        self._qt_path.setElementPositionAt(index, pos_x, pos_y)

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self._qt_object)

    ######## PRIVATE METHODS ########

    def _update_qt_object_path(self):
        """Synchronize the contents of self._qt_path to self._qt_object

        Returns: None
        """
        self._qt_object.setPath(self._qt_path)
