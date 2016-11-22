from brown.interface.path_interface import PathInterface
from brown.core.graphic_object import GraphicObject
from brown.utils.point import Point
from brown.utils.units import GraphicUnit
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
        self.elements = []

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
        if self.elements:
            return self.elements[-1].pos_relative_to_item(self)
        else:
            return Point.with_unit((0, 0), unit=GraphicUnit)

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

    def line_to(self, pos, parent=None):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `x` and `y`, and move `self.current_path_position` to the new point.

        Args:
            pos (Point or tuple): The target position
            parent (GraphicObject or None):

        Returns: None
        """
        rel_pos = Point(pos)
        if parent is None or parent == self:  # parent == self
            self._interface.line_to(rel_pos)
            if not len(self.elements):
                # HACK: Append initial move_to
                self.elements.append(PathElement(
                    self._interface.element_at(0), self, self))
            self.elements.append(PathElement(
                self._interface.element_at(-1), self, self))
        else:
            # HACK: Add some arbitrary offset to the temporary line-to
            #       position so that Qt doesn't convert it into a move-to
            #       (see note at top of path_interface).
            #       This could be avoided by either:
            #         1) Fixing this Qt bug (feature?) in path_interface
            #         2) Calculating the target line_to position directly
            #            here, probably saving a bit of efficiency too.
            #       (probably should do both)
            self._interface.line_to((float(self.pos.x) + 1,
                                     float(self.pos.x) + 1))
            if not len(self.elements):
                # HACK: Append initial move_to
                self.elements.append(PathElement(
                    self._interface.element_at(0), self, self))
            self.elements.append(PathElement(
                self._interface.element_at(-1), parent, self))
            self.elements[-1].pos = rel_pos
            self.elements[-1]._update_element_interface_pos()

    def cubic_to(self, control_1, control_2, end, parent=None):
        """Draw a cubic spline from the current position to a new point.

        Moves `self.current_path_position` to the new end point.

        Args:
            control_1_x (Point): The local position of the 1st control point
            control_2_x (Point): The local position of the 2nd control point
            end_x (Point): The local position of the end point
            parent (GraphicObject or None):

        Returns: None
        """
        # Ensure end_pos is a well-formed Point because it's needed to update
        # self.current_path_position
        rel_pos = Point(end)
        if parent is None:
            self._interface.cubic_to(
                control_1,
                control_2,
                rel_pos)
            # TODO: Need to append control points to elements list as well
            self.elements.append(PathElement(
                self._interface.element_at(-1), self, self))
        else:
            raise NotImplementedError
            self._interface.cubic_to(
                control_1,
                control_2,
                rel_pos)  # TODO: How to handle parentage with curves?
            self.elements.append(PathElement(
                self._interface.element_at(-1), parent, self))
            self.elements[-1].pos = rel_pos

    def move_to(self, pos, parent=None):
        """Close the current sub-path and start a new one.

        Args:
            pos (Point or tuple): The target position

        Returns: None
        """
        rel_pos = Point(pos)
        if parent is None:
            self._interface.move_to(rel_pos)
            self.elements.append(PathElement(
                self._interface.element_at(-1), self, self))
        else:
            raise NotImplementedError

    def close_subpath(self, parent=None):
        """Close the current sub-path and start a new one at (0, 0).

        This is equivalent to `move_to(0, 0)`

        Returns: None
        """
        self.move_to((0, 0), parent)
