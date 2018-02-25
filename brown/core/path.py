from brown import constants
from brown.core.brush import Brush
from brown.core.graphic_object import GraphicObject
from brown.core.path_element import PathElement
from brown.core.path_element_type import PathElementType
from brown.interface.path_interface import PathInterface
from brown.utils.exceptions import IllegalNumberOfControlPointsError
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class Path(GraphicObject):

    """A vector path whose points can be anchored to other objects.

    If a Path is in a `Flowable`, any point anchors in the path
    should be anchored to objects in the same `Flowable`, or
    undefined behavior may occur. Likewise, if a Path is not
    in a `Flowable`, all point anchors should not be in one either.
    """

    _default_brush = Brush(constants.DEFAULT_PATH_BRUSH_COLOR,
                           constants.DEFAULT_BRUSH_PATTERN)

    def __init__(self, pos, pen=None, brush=None, parent=None):
        """
        Args:
            pos (Point or init tuple): The position of the path root.
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None
        """
        super().__init__(pos, GraphicUnit(0), pen, brush, parent)
        self._current_draw_pos = Point(GraphicUnit(0), GraphicUnit(0))
        self.elements = []

    ######## CLASSMETHODS ########

    @classmethod
    def straight_line(cls, start, stop, pen=None, brush=None, parent=None):
        """Path: Constructor for a straight line

        Args:
            start (Point or init tuple): Starting position relative to the parent
            stop (Point or init tuple): Ending position relative to the parent.
            pen (Pen): The pen to draw outlines with.
            brush (Brush): The brush to draw outlines with.
            parent (GraphicObject): The parent object or None

        Returns: Path
        """
        line = cls(start, pen, brush, parent)
        if isinstance(stop, tuple):
            stop = Point(*stop)
        line.line_to(stop.x, stop.y)
        return line

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self):
        """Unit: The breakable length of the path.

        This is calculated automatically from path contents. By extension,
        this means that by default all `Path` objects will automatically
        wrap in `Flowable`s.
        """
        # Find the positions of every path element relative to the path
        min_x = GraphicUnit(float("inf"))
        max_x = GraphicUnit(-float("inf"))
        in_flowable = self.flowable is not None
        for element in self.elements:
            if in_flowable:
                relative_x = (self.flowable.pos_in_flowable_of(element)
                              - self.flowable.pos_in_flowable_of(self)).x
            else:
                relative_x = GraphicObject.map_between_items(self, element).x
            if relative_x > max_x:
                max_x = relative_x
            if relative_x < min_x:
                min_x = relative_x
        return max_x - min_x

    @property
    def current_draw_pos(self):
        """Point: The current drawing position relative to `self.pos`.

        This is the location from which operations like `line_to()` will draw.

        To change this without connecting the path to the new position,
        use `move_to()`.
        """
        if self.elements:
            if self.flowable is not None:
                return self.flowable.map_between_locally(
                    self, self.elements[-1])
            else:
                return GraphicObject.map_between_items(
                    self, self.elements[-1])
        else:
            return Point(GraphicUnit(0), GraphicUnit(0))

    ######## Public Methods ########

    def line_to(self, x, y, parent=None):
        """Draw a path from the current position to a new point.

        Connect a path from the current position to a new position specified
        by `x` and `y`, and move `self.current_draw_pos` to the new point.

        A point parent may be passed as well, anchored the target point to
        a separate GraphicObject. In this case, the coordinates passed will be
        considered relative to the parent.

        Args:
            x (Unit): The end x position
            y (Unit): The end y position
            parent (GraphicObject or Page): An optional parent, whose position
                the target coordinate will be relative to.

        Returns: None
        """
        if len(self.elements) == 0:
            self.move_to(GraphicUnit(0), GraphicUnit(0))
        self.elements.append(
            PathElement(Point(x, y),
                        PathElementType.line_to,
                        self,
                        parent if parent else self))

    def move_to(self, x, y, parent=None):
        """Close the current sub-path and start a new one.

        A point parent may be passed as well, anchored the target point to
        a separate `GraphicObject`. In this case, the coordinates passed will be
        considered relative to the parent.

        Args:
            x (Unit): The end x position
            y (Unit): The end y position
            parent (GraphicObject or Page): An optional parent, whose position
                the target coordinate will be relative to.

        Returns: None
        """
        self.elements.append(
            PathElement(Point(x, y),
                        PathElementType.move_to,
                        self,
                        parent if parent else self))

    def close_subpath(self):
        """Close the current sub-path and start a new one at the local origin.

        This is equivalent to `move_to((Unit(0), Unit(0)))`

        Returns: None

        Note:
            This convenience method does not support point parentage.
            If you need to anchor the new point, use an explicit
            `move_to((Unit(0), Unit(0)), parent)` instead.
        """
        self.move_to(GraphicUnit(0), GraphicUnit(0))

    def cubic_to(self,
                 control_1_x, control_1_y,
                 control_2_x, control_2_y,
                 end_x, end_y,
                 control_1_parent=None,
                 control_2_parent=None,
                 end_parent=None):
        """Draw a cubic bezier curve from the current position to a new point.

        Args:
            control_1_x (Unit): The x coordinate of the first control point.
            control_1_y (Unit): The y coordinate of the first control point.
            control_2_x (Unit): The x coordinate of the second control point.
            control_2_y (Unit): The y coordinate of the second control point.
            end_x (Unit): The x coordinate of the curve target.
            end_y (Unit): The y coordinate of the curve target.
            control_1_parent (GraphicObject or Page): An optional parent for
                the first control point. Defaults to `self`.
            control_2_parent (GraphicObject or Page): An optional parent for
                the second control point. Defaults to `self`.
            end_parent (GraphicObject or Page): An optional parent for the
                curve target. Defaults to `self`.

        Returns: None
        """
        if len(self.elements) == 0:
            self.move_to(GraphicUnit(0), GraphicUnit(0))
        self.elements.append(PathElement(Point(control_1_x, control_1_y),
                                         PathElementType.control_point,
                                         self,
                                         (control_1_parent if control_1_parent
                                          else self)))
        self.elements.append(PathElement(Point(control_2_x, control_2_y),
                                         PathElementType.control_point,
                                         self,
                                         (control_2_parent if control_2_parent
                                          else self)))
        self.elements.append(PathElement(Point(end_x, end_y),
                                         PathElementType.curve_to,
                                         self,
                                         (end_parent if end_parent
                                          else self)))

    def _render_slice(self, pos, clip_start_x=None, clip_width=None):
        """Render a horizontal slice of a path.

        If this proves to be a performance bottleneck in the future,
        it is very possible to optimize this to create `PathInterface`s
        which reuse `QPainterPath`s.

        Args:
            pos (Point): The doc-space position of the slice beginning
                (at the top-left corner of the slice)
            clip_start_x (Unit): The starting x position in the path
                of the slice
            clip_width (Unit): The horizontal length of the slice to
                be rendered

        Returns: None
        """
        slice_interface = PathInterface(
            self,
            pos,
            self.pen._interface,
            self.brush._interface,
            clip_start_x=clip_start_x,
            clip_width=clip_width)
        # Maintain a buffer of control points to be sent to the PathInterface
        control_point_buffer = []
        for element in self.elements:
            # Interface drawing methods expect coordinates
            # relative to PathInterface root
            if element.parent != self:
                if self.flowable is not None:
                    relative_pos = self.flowable.map_between_locally(
                        self, element)
                else:
                    relative_pos = GraphicObject.map_between_items(
                        self, element)
            else:
                relative_pos = element.pos
            if element.element_type == PathElementType.move_to:
                slice_interface.move_to(relative_pos)
            elif element.element_type == PathElementType.line_to:
                slice_interface.line_to(relative_pos)
            elif element.element_type == PathElementType.curve_to:
                if len(control_point_buffer) == 2:
                    slice_interface.cubic_to(*control_point_buffer,
                                             relative_pos)
                else:
                    raise IllegalNumberOfControlPointsError(
                        len(control_point_buffer))
                control_point_buffer = []
            elif element.element_type == PathElementType.control_point:
                control_point_buffer.append(relative_pos)
            else:
                raise AssertionError('Unknown element_type in Path')
        slice_interface.update_geometry()
        slice_interface.render()
        self.interfaces.add(slice_interface)

    def _render_complete(self, pos, dist_to_line_start=None, local_start_x=None):
        self._render_slice(pos, None, None)

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        self._render_slice(start, GraphicUnit(0), stop.x - start.x)

    def _render_after_break(self, local_start_x, start, stop):
        self._render_slice(start, local_start_x, stop.x - start.x)

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_slice(start, local_start_x, stop.x - start.x)
