from brown.interface.path_interface import PathInterface
from brown.core.graphic_object import GraphicObject
from brown.utils.point import Point
from brown.utils.anchored_point import AnchoredPoint
from brown.utils.units import GraphicUnit
from brown.core.path_element import PathElement
from brown.utils.path_element_type import PathElementType


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
        super().__init__(pos, 0, pen, brush, parent)
        self._current_path_position = Point(0, 0)
        self.elements = []
        self._interface = []

    ######## CLASSMETHODS ########

    @classmethod
    def straight_line(cls, start, stop, pen=None, brush=None, parent=None):
        """Path: Constructor for a straight line

        # TODO: Should parentable points be supported here?

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
    def breakable_width(self):
        """Unit: The breakable_width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        # TODO: Currently may not work for anchored elements
        return max(el.x for el in self.elements)

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
            return Path.map_between_items(self, self.elements[-1])
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

    def line_to(self, *args):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `x` and `y`, and move `self.current_path_position` to the new point.

        A point parent may be passed as well, anchored the target point to
        a separate GraphicObject. In this case, the coordinates passed will be
        considered relative to the parent.

        *args:
            Any valid set of args to initialize an AnchoredPoint:
            - An `x, y` pair outside of a tuple (parent will be None)
            - An `(x, y)` pair (parent will be None)
            - An `x, y, parent` triple outside of a tuple
            - An `(x, y, parent)` 3-tuple
            - An `(x, y)` pair and a `parent`
            - An `Point` and a `parent`
            - An existing `AnchoredPoint`
            - An existing `Point` (parent will be None)

        Returns: None
        """
        point = AnchoredPoint(*args)
        if point.parent is None:
            point.parent = self
        if len(self.elements) == 0:
            self.elements.append(PathElement((0, 0), PathElementType.move_to,
                                             self, self))
        self.elements.append(PathElement(point, PathElementType.line_to,
                                         self, point.parent))

    def move_to(self, *args):
        """Close the current sub-path and start a new one.

        A point parent may be passed as well, anchored the target point to
        a separate GraphicObject. In this case, the coordinates passed will be
        considered relative to the parent.

        *args:
            Any valid set of args to initialize an AnchoredPoint:
            - An `x, y` pair outside of a tuple (parent will be None)
            - An `(x, y)` pair (parent will be None)
            - An `x, y, parent` triple outside of a tuple
            - An `(x, y, parent)` 3-tuple
            - An `(x, y)` pair and a `parent`
            - An `Point` and a `parent`
            - An existing `AnchoredPoint`
            - An existing `Point` (parent will be None)

        Returns: None
        """
        point = AnchoredPoint(*args)
        if point.parent is None:
            point.parent = self
        self.elements.append(PathElement(point, PathElementType.move_to,
                                         self, point.parent))

    def close_subpath(self):
        """Close the current sub-path and start a new one at (0, 0).

        This is equivalent to `move_to((0, 0))`

        Returns: None

        Note:
            This convenience method does not support point parentage.
            If you need to anchor the new move_to point, use an explicit
            move_to((0, 0), parent) instead.
        """
        self.move_to((0, 0))

    def quad_to(self, control, end):
        """Draw a quadratic bezier curve from the current position to a new point.

        Moves `self.current_path_position` to the new end point.

        Args:
            control_1 (Point, AnchoredPoint, or tuple): The position of the
                1st control point with an optional parent. If a parent is
                provided, the coordinate will be relative to that.
            end (Point, AnchoredPoint, or tuple): The position of the
                1st control point with an optional parent. If a parent is
                provided, the coordinate will be relative to that.

        Returns: None

        Notes:
            The points may be passed in any valid set of initialization
            arguments for AnchoredPoint objects. See the docs on AnchoredPoint
            for a more thorough explanation.
        """
        # TODO: Implement me! (Priority Low)
        raise NotImplementedError

    def cubic_to(self, control_1, control_2, end):
        """Draw a cubic bezier curve from the current position to a new point.

        Moves `self.current_path_position` to the new end point.

        Args:
            control_1 (Point, AnchoredPoint, or tuple): The position of the
                1st control point with an optional parent. If a parent is
                provided, the coordinate will be relative to that.
            control_2 (Point, AnchoredPoint, or tuple): The position of the
                2nd control point with an optional parent. If a parent is
                provided, the coordinate will be relative to that.
            end (Point, AnchoredPoint, or tuple): The position of the
                1st control point with an optional parent. If a parent is
                provided, the coordinate will be relative to that.

        Returns: None

        Notes:
            The points may be passed in any valid set of initialization
            arguments for AnchoredPoint objects. See the docs on AnchoredPoint
            for a more thorough explanation.
        """
        if len(self.elements) == 0:
            self.elements.append(PathElement((0, 0), PathElementType.move_to,
                                             self, self))
        norm_control_1 = AnchoredPoint(control_1)
        norm_control_2 = AnchoredPoint(control_2)
        norm_end = AnchoredPoint(end)
        for point in [norm_control_1, norm_control_2, norm_end]:
            if not point.parent:
                point.parent = self
        self.elements.append(PathElement(norm_control_1,
                                         PathElementType.control_point,
                                         self, point.parent))
        self.elements.append(PathElement(norm_control_2,
                                         PathElementType.control_point,
                                         self, point.parent))
        self.elements.append(PathElement(norm_end,
                                         PathElementType.curve_to,
                                         self, point.parent))

    def _render_slice(self, pos, start_x=None, length=None):
        """Render a horizontal slice of a path.

        Args:
            pos (Point): The doc-space position of the slice beginning
                (at the top-left corner of the slice)
            start_x (Unit): The starting x position in the path of the slice
            length (Unit): The horizontal length of the slice to be rendered

        Returns: None
        """
        print('rendering slice at {} from local_x {} with length {}'.format(pos, start_x, length))
        if start_x is None:
            start_x = 0
        adjusted_pos = Point(pos.x - start_x, pos.y)
        self._interface = self._interface_class(
            pos=adjusted_pos,
            pen=self.pen._interface if self.pen else None,
            brush=self.brush._interface if self.brush else None,
            # Don't pass parent as part of experimental shift away from interface parentage
            # self.parent._interface if self.parent else None,
            clip_start_x=start_x,
            clip_width=length)
        # Position calculations will probably have to be made in reference
        # to doc-space position of points in case of AnchoredPoints,
        # so this will probably need to be revisited
        for element in self.elements:
            if element.parent != self:
                relative_pos = self.map_between_items(self, element)
                import pdb; pdb.set_trace()
            else:
                relative_pos = element.pos
            if element.element_type == PathElementType.move_to:
                self._interface.move_to(relative_pos)
            elif element.element_type == PathElementType.line_to:
                self._interface.line_to(relative_pos)
            elif element.element_type == PathElementType.curve_to:
                self._interface.curve_to(relative_pos)
            elif element.element_type == PathElementType.control_point:
                self._interface.control_point(relative_pos)
            else:
                raise AssertionError('Unknown element_type in Path')
        self._interface.render()

    def _render_complete(self, pos):
        print('_render_complete()')
        self._render_slice(pos, start_x=None, length=None)

    def _render_before_break(self, local_start_x, start, stop):
        print('_render_before_break()')
        self._render_slice(start, local_start_x, stop.x - start.x)

    def _render_after_break(self, local_start_x, start, stop):
        print('_render_after_break()')
        self._render_slice(start, local_start_x, stop.x - start.x)

    def _render_spanning_continuation(self, local_start_x, start, stop):
        print('_render_spanning_continuation()')
        self._render_slice(start, local_start_x, stop.x - start.x)
