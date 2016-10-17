from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from brown.core import brown
from brown.interface.abstract.path_interface import PathInterface


class PathInterfaceQt(PathInterface):
    """Interface for a generic graphic path object."""
    def __init__(self, x, y):
        """
        Args:
            x (float): The x position of the path relative to the document
            y (float): The y position of the path relative to the document
        """
        self.x = x
        self.y = y
        self.current_path_x = 0
        self.current_path_y = 0
        self._qt_object = QtGui.QPainterPath(
            QtCore.QPointF(self.current_path_x, self.current_path_y))

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

    @property
    def y(self):
        """
        float: The y position of the Path relative to the document
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def current_path_position(self):
        """
        tuple (float: x, float: y): The current relative drawing position.

        This is the location from which operations like line_to() will draw,
        relative to the position of the Path (`self.x` and `self.y`).

        This value is dependent on `self.current_path_x` and
        `self.current_path_y`, both of which are initialized to `0`.
        """
        return self.current_path_x, self.current_path_y

    @current_path_position.setter
    def current_path_position(self, position):
        self.current_path_x, self.current_path_y = position

    @property
    def current_path_x(self):
        """
        float: The current relative drawing x-axis position
        """
        return self._current_path_x

    @current_path_x.setter
    def current_path_x(self, value):
        self._current_path_x = value

    @property
    def current_path_y(self):
        """
        float: The current relative drawing x-axis position
        """
        return self._current_path_y

    @current_path_y.setter
    def current_path_y(self, value):
        self._current_path_y = value

    ######## Public Methods ########

    def line_to(self, x, y):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `x` and `y`, and move `self.current_path_position` to the new point.

        Args:
            x (float): The relative x-axis position of the line endpoint
            y (float): The relative y-axis position of the line endpoint

        Returns: None
        """
        self._qt_object.lineTo(x, y)
        self.current_path_position = (x, y)

    def cubic_to(self,
                 control_1_x, control_1_y,
                 control_2_x, control_2_y,
                 end_x, end_y):
        """Draw a cubic spline from the current position to a new point.

        Moves `self.current_path_position` to the new end point.

        Args:
            control_1_x (float): The x position of the first control point
            control_1_y (float): The y position of the first control point
            control_2_x (float): The x position of the second control point
            control_2_y (float): The y position of the second control point
            end_x (float): The x position of the end point
            end_y (float): The y position of the end point

        Returns:
            None
        """
        self._qt_object.cubicTo(
            control_1_x, control_1_y,
            control_2_x, control_2_y,
            end_x, end_y)

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        # Note: This seems to implicitly convert the QPainterPath
        # to a QGraphicsPathItem, and add that to the scene.
        # Might cause difficulty down the line.
        brown._app_interface.scene.addPath(self._qt_object)
