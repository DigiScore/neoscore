from abc import ABC


class PathInterface(ABC):
    """Interface for a generic graphic path object."""
    def __init__(self, x, y, pen=None, brush=None):
        """
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
        raise NotImplementedError

    @x.setter
    def x(self, value):
        raise NotImplementedError

    @property
    def y(self):
        """
        float: The y position of the Path relative to the document
        """
        raise NotImplementedError

    @y.setter
    def y(self, value):
        raise NotImplementedError

    @property
    def pen(self):
        """
        PenInterface: The pen to draw outlines with
        """
        raise NotImplementedError

    @pen.setter
    def pen(self, value):
        raise NotImplementedError

    @property
    def brush(self):
        """
        BrushInterface: The brush to draw outlines with
        """
        raise NotImplementedError

    @brush.setter
    def brush(self, value):
        raise NotImplementedError

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
        raise NotImplementedError

    @property
    def current_path_x(self):
        """
        float: The current relative drawing x-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        raise NotImplementedError

    @property
    def current_path_y(self):
        """
        float: The current relative drawing x-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def move_to(self, new_x, new_y):
        """Close the current sub-path and start a new one.

        Args:
            new_x: The new x coordinate to begin the new sub-path
            new_y: The new y coordinate to begin the new sub-path

        Returns: None
        """
        raise NotImplementedError

    def render(self):
        """Render the line to the scene.

        Returns: None
        """
        raise NotImplementedError
