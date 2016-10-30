from brown.interface.path_interface import PathInterface
from brown.core.graphic_object import GraphicObject


class Path(GraphicObject):

    _interface_class = PathInterface

    def __init__(self, x, y, pen=None, brush=None, parent=None):
        """
        Args:
            x (float): The x position of the path relative to the document
            y (float): The y position of the path relative to the document
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent: The parent (core-level) object or None
        """
        # Hack? Initialize interface to position 0, 0
        # so that attribute setters don't try to push
        # changes to not-yet-existing interface

        self._interface = Path._interface_class(0, 0)
        super().__init__(x, y, pen, brush, parent)
        self._current_path_x = 0
        self._current_path_y = 0

    ######## CLASSMETHODS ########

    @classmethod
    def straight_line(cls, x_start, y_start, delta_x, delta_y, parent=None):
        # TODO: This is pretty awkward, it may well be more intuitive to
        #       to (startx, starty, endx, endy) instead
        line = cls(x_start, y_start, parent=parent)
        line.line_to(delta_x, delta_y)
        return line

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
            x (float): The relative x-axis position of the line endpoint
            y (float): The relative y-axis position of the line endpoint

        Returns: None
        """
        self._interface.line_to(x, y)

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

        Returns: None
        """
        self._interface.cubic_to(
            control_1_x, control_1_y,
            control_2_x, control_2_y,
            end_x, end_y)

    def move_to(self, new_x, new_y):
        """Close the current sub-path and start a new one.

        Args:
            new_x: The new x coordinate to begin the new sub-path
            new_y: The new y coordinate to begin the new sub-path

        Returns: None
        """
        self._interface.move_to(new_x, new_y)
        self._current_path_x = new_x
        self._current_path_y = new_y

    def close_subpath(self):
        """Close the current sub-path and start a new one at (0, 0).

        This is equivalent to `move_to(0, 0)`

        Returns: None
        """
        self._interface.close_subpath
        self._current_path_y = 0
        self._current_path_x = 0
