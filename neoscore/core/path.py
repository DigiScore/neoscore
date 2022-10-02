from __future__ import annotations

from math import atan, cos, pi, sin, sqrt, tan
from typing import List, Optional, Tuple, cast

from neoscore.core.brush import Brush, BrushDef
from neoscore.core.layout_controllers import NewLine
from neoscore.core.painted_object import PaintedObject
from neoscore.core.path_element import (
    ControlPoint,
    CurveTo,
    LineTo,
    MoveTo,
    PathElement,
)
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import ORIGIN, Point, PointDef
from neoscore.core.positioned_object import PositionedObject, render_cached_property
from neoscore.core.units import ZERO, Mm, Unit
from neoscore.interface.path_interface import (
    PathInterface,
    ResolvedCurveTo,
    ResolvedLineTo,
    ResolvedMoveTo,
    ResolvedPathElement,
)

_TWO_PI = pi * 2
_HALF_PI = pi / 2


class Path(PaintedObject):

    """A vector path whose elements can be anchored to other objects.

    If a ``Path`` is in a :obj:`.Flowable`, any element parents in the path should be in the
    same flowable. Likewise, if a path is not in a flowable, all element parts should
    not be in one either.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        rotation: float = 0,
        background_brush: Optional[BrushDef] = None,
        transform_origin: PointDef = ORIGIN,
    ):
        """
        Args:
            pos: The position of the path root.
            parent: The parent object or None
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
            rotation: Angle in degrees. Rotated paths with flowable breaks or
                path elements parented to other objects are not currently supported.
            background_brush: Optional brush used to paint the path's bounding rect
                behind it.
        """
        super().__init__(pos, parent, brush, pen)
        self.background_brush = background_brush
        self._rotation = rotation
        self.elements: List[PathElement] = []
        self._current_subpath_start: Optional[Tuple[Point, Optional[parent]]] = None
        self.transform_origin = transform_origin

    @classmethod
    def straight_line(
        cls,
        start: PointDef,
        parent: Optional[PositionedObject],
        end: PointDef,
        end_parent: Optional[PositionedObject] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ) -> Path:
        """Convenience for drawing a single straight line.

        Args:
            start: The position of the center of the arrow line's start
            parent: A parent object
            end: The position of the end of the line, relative to ``end_parent``
                if provided or otherwise ``start``
            end_parent: An optional parent for the end point.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with. Defaults to no pen.
        """
        line = cls(start, parent, brush, pen)
        end = Point.from_def(end)
        line.line_to(end.x, end.y, end_parent)
        return line

    @classmethod
    def rect(
        cls,
        pos: PointDef,
        parent: Optional[PositionedObject],
        width: Unit,
        height: Unit,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """Convenience for drawing a rectangle."""
        path = cls(pos, parent, brush, pen)
        path.line_to(width, ZERO)
        path.line_to(width, height)
        path.line_to(ZERO, height)
        path.line_to(ZERO, ZERO)
        return path

    @classmethod
    def ellipse(
        cls,
        pos: PointDef,
        parent: Optional[PositionedObject],
        width: Unit,
        height: Unit,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """Convenience for drawing an ellipse.

        ``pos`` indicates the top left corner of the ellipse's bounding rect.
        To create a path from a center point, use ``Path.ellipse_from_center``.

        This can also be used for drawing circles by giving the same width and height.
        """
        # Algorithm courtesy of https://stackoverflow.com/a/2173084/5615927
        path = cls(pos, parent, brush, pen)
        kappa = 0.5522848
        ox = (width / 2) * kappa  # control point offset horizontal
        oy = (height / 2) * kappa  # control point offset vertical
        xe = width  # x-end
        ye = height  # y-end
        xm = width / 2  # x-middle
        ym = height / 2  # y-middle
        path.move_to(ZERO, ym)
        path.cubic_to(ZERO, ym - oy, xm - ox, ZERO, xm, ZERO)
        path.cubic_to(xm + ox, ZERO, xe, ym - oy, xe, ym)
        path.cubic_to(xe, ym + oy, xm + ox, ye, xm, ye)
        path.cubic_to(xm - ox, ye, ZERO, ym + oy, ZERO, ym)
        return path

    @classmethod
    def ellipse_from_center(
        cls,
        center_pos: PointDef,
        parent: Optional[PositionedObject],
        width: Unit,
        height: Unit,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """Convenience for drawing an ellipse from its center point.

        The constructed path will have its ``pos`` at the ellipse bounding rect's top
        left corner.

        See also ``Path.ellipse``
        """
        center_pos = Point.from_def(center_pos)
        return Path.ellipse(
            Point(center_pos.x - (width / 2), center_pos.y - (height / 2)),
            parent,
            width,
            height,
            brush,
            pen,
        )

    @classmethod
    def arc(
        cls,
        pos: PointDef,
        parent: Optional[PositionedObject],
        width: Unit,
        height: Unit,
        start_angle: float,
        stop_angle: float,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """Convenience for drawing an elliptical arc.

        Args:
            pos: The position of the upper left corner of the traced ellipse. parent:
                The parent object or None width: The traced ellipse's width height: The
                traced ellipse's height start_angle: The starting arc angle in radians
                clockwise relative
                to the 3 o'clock position.
            parent: The parent object or None
            width: The full ellipse width
            height: The full ellipse height
            start_angle: The start arc angle in radians clockwise relative
                to the 3 o'clock position.
            stop_angle: The stopping arc angle, defined like ``start_angle``.
            brush: The brush to fill shapes with. pen: The pen to draw outlines with.
            pen: The pen to draw outlines with.

        The arc definition can be most easily understood as tracing an ellipse as
        defined in ``Path.ellipse()``, where ``pos`` marks the top-left corner of the
        ellipse bounding rect. Two angles are provided in clockwise radians relative to
        the 3 o'clock position. The arc is traced from ``start_angle`` clockwise to
        ``stop_angle``. Consequently, depending on the provided angles the actually
        drawn path may be far from the Path's position.

        The provided angles are interpreted mod ``2*pi``. The angle between them must
        not be 0. This also means arc angles of ``2*pi``, (i.e. complete ellipses), are
        not supported as they are interpreted as 0. Complete ellipses should instead be
        drawn with ``Path.ellipse()``.

        Raises:
            ValueError: if invalid angles are given
        """
        # This method and ``_acute_arc_to_bezier`` are adapted from Joe
        # Cridge's algorithm and JS implementation found at
        # https://www.joecridge.me/bezier.pdf. Most of the original
        # comments have been left in place as well.

        # Work in float base units, converting back to units at the end
        w = width.base_value
        h = height.base_value

        # Make all angles positive...
        while start_angle < 0:
            start_angle += _TWO_PI
        while stop_angle < 0:
            stop_angle += _TWO_PI

        # ...and confine them to the interval [0,TWO_PI).
        start_angle %= _TWO_PI
        stop_angle %= _TWO_PI

        # Adjust angles to counter linear scaling.
        if start_angle <= _HALF_PI:
            start_angle = atan(w / h * tan(start_angle))
        elif _HALF_PI < start_angle <= 3 * _HALF_PI:
            start_angle = atan(w / h * tan(start_angle)) + pi
        else:
            start_angle = atan(w / h * tan(start_angle)) + _TWO_PI
        if stop_angle <= _HALF_PI:
            stop_angle = atan(w / h * tan(stop_angle))
        elif _HALF_PI < stop_angle <= 3 * _HALF_PI:
            stop_angle = atan(w / h * tan(stop_angle)) + pi
        else:
            stop_angle = atan(w / h * tan(stop_angle)) + _TWO_PI

        # Exceed the interval if necessary in order to preserve the size and
        # orientation of the arc.
        if start_angle > stop_angle:
            stop_angle += _TWO_PI

        # Create curves
        epsilon = 0.00001  # Smallest visible angle on displays up to 4K.
        curves = []
        while stop_angle - start_angle > epsilon:
            arc_to_draw = min(stop_angle - start_angle, _HALF_PI)
            curves.append(Path._acute_arc_to_bezier(start_angle, arc_to_draw))
            start_angle += arc_to_draw

        if not len(curves):
            raise ValueError(f"Invalid arc angles {start_angle} and {stop_angle}.")

        # Draw curves
        path = cls(pos, parent, brush, pen)
        rx = w / 2.0
        ry = h / 2.0
        path.move_to(Unit(rx * curves[0]["ax"] + rx), Unit(ry * curves[0]["ay"] + ry))
        for curve in curves:
            path.cubic_to(
                Unit(rx * curve["bx"] + rx),
                Unit(ry * curve["by"] + ry),
                Unit(rx * curve["cx"] + rx),
                Unit(ry * curve["cy"] + ry),
                Unit(rx * curve["dx"] + rx),
                Unit(ry * curve["dy"] + ry),
            )
        return path

    @staticmethod
    def _acute_arc_to_bezier(start: float, size: float) -> dict:
        """
        Generate a cubic Bezier representing an arc on the unit circle of total
        angle ``size`` radians, beginning ``start`` radians above the x-axis.
        """
        # Evaluate constants.
        alpha = size / 2.0
        cos_alpha = cos(alpha)
        sin_alpha = sin(alpha)
        cot_alpha = 1.0 / tan(alpha)
        phi = start + alpha  # This is how far the arc needs to be rotated.
        cos_phi = cos(phi)
        sin_phi = sin(phi)
        lambda_ = (4.0 - cos_alpha) / 3.0
        mu = sin_alpha + (cos_alpha - lambda_) * cot_alpha
        # Return rotated waypoints.
        return {
            "ax": cos(start),
            "ay": sin(start),
            "bx": lambda_ * cos_phi + mu * sin_phi,
            "by": lambda_ * sin_phi - mu * cos_phi,
            "cx": lambda_ * cos_phi - mu * sin_phi,
            "cy": lambda_ * sin_phi + mu * cos_phi,
            "dx": cos(start + size),
            "dy": sin(start + size),
        }

    @classmethod
    def arrow(
        cls,
        start: PointDef,
        parent: Optional[PositionedObject],
        end: PointDef,
        end_parent: Optional[PositionedObject] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        line_width: Unit = Mm(0.35),
        arrow_head_width: Unit = Mm(1.5),
        arrow_head_length: Unit = Mm(2.5),
    ) -> Path:
        """Convenience for drawing an arrow

        Args:
            start: The position of the center of the arrow line's start
            parent: A parent object
            end: The position of the arrow's tip, relative to ``end_parent``
                if provided or ``start``
            end_parent: An optional parent for the end point.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with. Defaults to no pen.
            line_width: The thickness of the arrow's line
            arrow_head_width: The width of the arrow head extending perpendicular
                from the line.
            arrow_head_length: The length of the arrow head parallel to the line.

        Note that ``end_parent`` is only used for initially drawing the
        path. If ``end_parent`` moves relative to the path after
        creation, the path shape will not be automatically updated.
        """
        # This algorithm is lightly adapted from
        # https://github.com/frogcat/canvas-arrow by Yuzo Matsuzawa
        # released under MIT.
        path = cls(start, parent, brush, pen or Pen.no_pen())
        end = Point.from_def(end)
        if end_parent:
            end = path.map_to(end_parent) + end
        # The original algorithm supports diverse shapes, including
        # things like double-headed arrows, using this system of a
        # variable numbers of control points. We don't use them right
        # now, but since we might want to later (and since I don't
        # understand the code enough to refactor it) it's left in
        # place here.
        control_points = [
            (0, line_width.base_value / 2),
            (-arrow_head_length.base_value, line_width.base_value / 2),
            (-arrow_head_length.base_value, arrow_head_width.base_value / 2),
        ]
        # The start pos (relative to the path) is always (0, 0), so dx
        # and dy are just the end position
        dx = end.x.base_value
        dy = end.y.base_value
        length = sqrt(dx * dx + dy * dy)
        sin_ = dy / length
        cos_ = dx / length
        resolved_points: List[Tuple[float, float]] = [(0, 0)]
        for cp in control_points:
            if cp[0] < 0:
                resolved_points.append((length + cp[0], cp[1]))
            else:
                resolved_points.append(cp)
        resolved_points.append((length, 0))
        for cp in reversed(control_points):
            if cp[0] < 0:
                resolved_points.append((length + cp[0], -cp[1]))
            else:
                resolved_points.append((cp[0], -cp[1]))
        resolved_points.append((0, 0))
        path.move_to(Unit(resolved_points[0][0]), Unit(resolved_points[0][1]))
        for rp in resolved_points[1:]:
            x = rp[0] * cos_ - rp[1] * sin_
            y = rp[0] * sin_ + rp[1] * cos_
            path.line_to(Unit(x), Unit(y))
        return path

    @render_cached_property
    def breakable_length(self) -> Unit:
        """The breakable length of the path.

        This is calculated automatically from path contents. By extension,
        this means that by default all ``Path`` objects will automatically
        wrap in flowables.
        """
        # Find the positions of every path element relative to the path
        min_x = Unit(float("inf"))
        max_x = Unit(-float("inf"))
        for element in self.elements:
            # Determine element X relative to self
            relative_x = self.map_x_to(element)
            # Now update min/max accordingly
            if relative_x > max_x:
                max_x = relative_x
            if relative_x < min_x:
                min_x = relative_x
        return max_x - min_x

    @property
    def background_brush(self) -> Optional[Brush]:
        """An optional brush to paint over the path bounding rect's background with"""
        return self._background_brush

    @background_brush.setter
    def background_brush(self, value: Optional[BrushDef]):
        if value:
            self._background_brush = Brush.from_def(value)
        else:
            self._background_brush = None

    def line_to(self, x: Unit, y: Unit, parent: Optional[PositionedObject] = None):
        """Draw a path from the current position to a new point.

        If the path is empty, this will add two elements, an initial
        ``MoveTo(ORIGIN, self)`` and the requested ``LineTo``.

        Args:
            x: The end x position
            y: The end y position
            parent: An optional parent, whose position the target coordinate
                will be relative to.

        """
        if not len(self.elements):
            self.move_to(ZERO, ZERO)
        self.elements.append(LineTo(Point(x, y), parent or self))

    def move_to(self, x: Unit, y: Unit, parent: Optional[PositionedObject] = None):
        """Close the current sub-path and start a new one.

        Args:
            x: The end x position
            y: The end y position
            parent: An optional parent, whose position the target coordinate will
                be relative to.
        """
        self._current_subpath_start = (Point(x, y), parent or self)
        self.elements.append(MoveTo(Point(x, y), parent or self))

    def close_subpath(self):
        """Close the current sub-path with a line.

        Draw a line back to the starting position (including any parent) of the current
        subpath.
        """
        end_pos = Point.from_def(self._current_subpath_start[0])
        end_parent = self._current_subpath_start[1]
        self.line_to(
            end_pos.x,
            end_pos.y,
            end_parent,
        )

    def cubic_to(
        self,
        control_1_x: Unit,
        control_1_y: Unit,
        control_2_x: Unit,
        control_2_y: Unit,
        end_x: Unit,
        end_y: Unit,
        control_1_parent: Optional[PositionedObject] = None,
        control_2_parent: Optional[PositionedObject] = None,
        end_parent: Optional[PositionedObject] = None,
    ):
        """Draw a cubic bezier curve from the current position to a new point.

        If the path is empty, this will add two elements, an initial
        ``MoveTo(ORIGIN, self)`` and the requested ``CurveTo``.

        Args:
            control_1_x: The x coordinate of the first control point.
            control_1_y: The y coordinate of the first control point.
            control_2_x: The x coordinate of the second control point.
            control_2_y: The y coordinate of the second control point.
            end_x: The x coordinate of the curve target.
            end_y: The y coordinate of the curve target.
            control_1_parent: An optional parent for
                the first control point. Defaults to ``self``.
            control_2_parent: An optional parent for
                the second control point. Defaults to ``self``.
            end_parent: An optional parent for the
                curve target. Defaults to ``self``.

        """
        c1 = ControlPoint(
            Point(control_1_x, control_1_y),
            control_1_parent or self,
        )
        c2 = ControlPoint(
            Point(control_2_x, control_2_y),
            control_2_parent or self,
        )
        if not len(self.elements):
            self.move_to(ZERO, ZERO)
        self.elements.append(CurveTo(Point(end_x, end_y), end_parent or self, c1, c2))

    def _relative_element_pos(self, element: PositionedObject) -> Point:
        return self.map_to(element)

    def _resolve_path_elements(self) -> List[ResolvedPathElement]:
        resolved: List[ResolvedPathElement] = []
        for element in self.elements:
            # Interface drawing methods expect coordinates
            # relative to PathInterface root
            pos = self._relative_element_pos(element)
            if isinstance(element, LineTo):
                resolved.append(ResolvedLineTo(pos.x, pos.y))
            elif isinstance(element, MoveTo):
                resolved.append(ResolvedMoveTo(pos.x, pos.y))
            elif isinstance(element, CurveTo):
                element = cast(CurveTo, element)
                resolved_c1_pos = self._relative_element_pos(element.control_1)
                resolved_c2_pos = self._relative_element_pos(element.control_2)
                resolved.append(
                    ResolvedCurveTo(
                        resolved_c1_pos.x,
                        resolved_c1_pos.y,
                        resolved_c2_pos.x,
                        resolved_c2_pos.y,
                        pos.x,
                        pos.y,
                    )
                )
            else:
                raise TypeError("Unknown PathElement type")
        return resolved

    def _render_slice(
        self,
        pos: Point,
        inside_flowable: bool,
        clip_start_x: Optional[Unit] = None,
        clip_width: Optional[Unit] = None,
    ):
        # If this proves to be a performance bottleneck in the future,
        # it is very possible to optimize this to create `PathInterface`s
        # which reuse `QPainterPath`s.
        resolved_path_elements = self._resolve_path_elements()
        slice_interface = PathInterface(
            pos,
            None if inside_flowable else self.parent.interface_for_children,
            self.scale,
            self.rotation,
            self.transform_origin,
            self.brush.interface,
            self.pen.interface,
            resolved_path_elements,
            self.background_brush.interface if self.background_brush else None,
            clip_start_x,
            clip_width,
        )
        slice_interface.render()
        self.interfaces.append(slice_interface)

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        inside_flowable = bool(flowable_line)
        self._render_slice(pos, inside_flowable, None, None)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        slice_length = flowable_line.length - (flowable_x - flowable_line.flowable_x)
        self._render_slice(pos, True, ZERO, slice_length)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        self._render_slice(pos, True, object_x, flowable_line.length)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        self._render_slice(pos, True, object_x, None)
