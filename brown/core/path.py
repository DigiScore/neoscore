from brown.interface.path_interface import PathInterface
from brown.core.graphic_object import GraphicObject
from brown.utils.point import Point
from brown.core.path_element import PathElement


class Path(GraphicObject):

    _interface_class = PathInterface

    def __init__(self, pos, pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point[GraphicUnit]): The position of the path relative
                to the document
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None
        """
        # Hack? Initialize interface to position 0, 0
        # so that attribute setters don't try to push
        # changes to not-yet-existing interface

        self._interface = Path._interface_class((0, 0))
        super().__init__(pos, pen, brush, parent)
        self._current_path_position = Point(0, 0)

    ######## CLASSMETHODS ########

    @classmethod
    def straight_line(cls, start, stop, pen=None, brush=None, parent=None):
        """Path: Constructor for a straight line

        Args:
            start (Point): Starting position relative to the parent
            stop (Point): Ending position relative to the parent.
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None

        Returns: Path
        """
        line = cls(start, pen, brush, parent)
        line.line_to(stop)
        return line

    ######## PUBLIC PROPERTIES ########

    @property
    def current_path_position(self):
        """
        Point[GraphicUnit]: The current relative drawing position.

        This is the location from which operations like line_to() will draw,
        relative to the position of the Path (`self.x` and `self.y`).

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self._current_path_position

    @property
    def current_path_x(self):
        """
        GraphicUnit: The current relative drawing x-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self.current_path_position.x

    @property
    def current_path_y(self):
        """
        GraphicUnit: The current relative drawing y-axis position

        This property is read-only. To move the current position, use
        the move_to() method, implicitly closing the current sub-path and
        beginning a new one.
        """
        return self.current_path_position.y

    ######## Public Methods ########


    def element_at(self, index):
        """Find the element at a given index and return it.

        Args:
            index (int): The element index. Use -1 for the last index.

        Returns: PathElementInterface

        # TODO: Implement a list-like iterable wrapper around path elements.
        """
        pass

    def set_element_position_at(self, index, pos):
        """Set the element at an index to a given position.

        Args:
            index (int): The element index to modify
            pos (Point[GraphicUnit] or tuple): The new position
                for the element.

        Returns: None
        """
        # TODO: Make index error guards when proper element list is made
        self._qt_path.setElementPositionAt(index, float(pos[0]), float(pos[0]))

    def line_to(self, pos):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `x` and `y`, and move `self.current_path_position` to the new point.

        Args:
            pos (Point or tuple): The target position

        Returns: None
        """
        target = Point(pos)
        self._interface.line_to(target)
        self.current_path_position.x = target.x
        self.current_path_position.y = target.y

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
        # Ensure end_pos is a well-formed Point because it's needed to update
        # self.current_path_position
        end_pos = Point(end)
        self._interface.cubic_to(
            control_1,
            control_2,
            end_pos)
        self.current_path_position.x = end_pos.x
        self.current_path_position.y = end_pos.y

    def move_to(self, pos):
        """Close the current sub-path and start a new one.

        Args:
            pos (Point or tuple): The target position

        Returns: None
        """
        target = Point(pos)
        self._interface.move_to(target)
        self.current_path_position.x = target.x
        self.current_path_position.y = target.y

    def close_subpath(self):
        """Close the current sub-path and start a new one at (0, 0).

        This is equivalent to `move_to(0, 0)`

        Returns: None
        """
        self._interface.close_subpath
        self.current_path_position.x = 0
        self.current_path_position.y = 0
