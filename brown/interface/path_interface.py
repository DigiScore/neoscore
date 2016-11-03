from PyQt5 import QtWidgets
from PyQt5 import QtGui

from brown.core import brown
from brown.interface.graphic_object_interface import GraphicObjectInterface


class PathInterface(GraphicObjectInterface):
    """Interface for a generic graphic path object."""
    def __init__(self, x, y, pen=None, brush=None, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the parent
            y (float): The y position of the path relative to the parent
            pen (PenInterface): The pen to draw outlines with.
            brush (BrushInterface): The brush to draw outlines with.
            parent (GraphicObjectInterface):
        """
        self._qt_path = QtGui.QPainterPath()
        self._qt_object = QtWidgets.QGraphicsPathItem(self._qt_path)
        self.x = x
        self.y = y
        self.pen = pen
        self.brush = brush
        self._current_path_x = 0
        self._current_path_y = 0
        self.parent = parent

    ######## PUBLIC PROPERTIES ########

    @property
    def current_path_position(self):
        """
        tuple (float: x, float: y): The current relative drawing position.

        This is the location from which operations like line_to() will draw,
        relative to the position of the Path (`self.x` and `self.y`).

        This value is dependent on `self.current_path_x` and
        `self.current_path_y`, both of which are initialized to `0`.

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self.current_path_x, self.current_path_y

    @property
    def current_path_x(self):
        """
        float: The current relative drawing x-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self._current_path_x

    @property
    def current_path_y(self):
        """
        float: The current relative drawing x-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self._current_path_y

    ######## Public Methods ########

    def line_to(self, x, y):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `x` and `y`, and move `self.current_path_position` to the new point.

        Args:
            x (float): The local x position of the line endpoint
            y (float): The local y position of the line endpoint

        Returns: None
        """
        self._qt_path.lineTo(x, y)
        self._update_qt_object_path()
        self._current_path_x = x
        self._current_path_y = y

    def cubic_to(self,
                 control_1_x, control_1_y,
                 control_2_x, control_2_y,
                 end_x, end_y):
        """Draw a cubic spline from the current position to a new point.

        Moves `self.current_path_position` to the new end point.

        Args:
            control_1_x (float): The local x position of the 1st control point
            control_1_y (float): The local y position of the 1st control point
            control_2_x (float): The local x position of the 2nd control point
            control_2_y (float): The local y position of the 2nd control point
            end_x (float): The local x position of the end point
            end_y (float): The local y position of the end point

        Returns: None
        """
        self._qt_path.cubicTo(
            control_1_x, control_1_y,
            control_2_x, control_2_y,
            end_x, end_y)
        self._update_qt_object_path()
        self._current_path_x = end_x
        self._current_path_y = end_y

    def move_to(self, new_x, new_y):
        """Close the current sub-path and start a new one.

        Args:
            new_x: The new x coordinate to begin the new sub-path
            new_y: The new y coordinate to begin the new sub-path

        Returns: None
        """
        self._qt_path.moveTo(new_x, new_y)
        self._current_path_x = new_x
        self._current_path_y = new_y
        self._update_qt_object_path()

    def close_subpath(self):
        """Close the current sub-path and start a new one at (0, 0).

        This is equivalent to `move_to(0, 0)`

        Returns: None
        """
        self._qt_path.closeSubpath()
        self._current_path_y = 0
        self._current_path_x = 0
        self._update_qt_object_path()

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        brown._app_interface.scene.addItem(self._qt_object)

    ######## PRIVATE METHODS ########

    def _update_qt_object_path(self):
        """
        Synchronize the contents of self._qt_path to self._qt_object
        """
        self._qt_object.setPath(self._qt_path)
