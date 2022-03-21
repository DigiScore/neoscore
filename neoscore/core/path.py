from __future__ import annotations

from math import atan, cos, pi, sin, sqrt, tan
from typing import TYPE_CHECKING, Optional, cast

from neoscore.core.brush import SimpleBrushDef
from neoscore.core.mapping import map_between, map_between_x
from neoscore.core.painted_object import PaintedObject
from neoscore.core.path_element import (
    ControlPoint,
    CurveTo,
    LineTo,
    MoveTo,
    PathElement,
)
from neoscore.core.pen import NO_PEN, SimplePenDef
from neoscore.interface.path_interface import (
    PathInterface,
    ResolvedCurveTo,
    ResolvedLineTo,
    ResolvedMoveTo,
    ResolvedPathElement,
)
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import ZERO, Mm, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Path(PaintedObject):

    """A vector path whose points can be anchored to other objects.

    If a Path is in a `Flowable`, any point anchors in the path
    should be anchored to objects in the same `Flowable`, or
    undefined behavior may occur. Likewise, if a Path is not
    in a `Flowable`, all point anchors should not be in one either.
    """

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent],
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """
        Args:
            pos: The position of the path root.
            parent: The parent object or None
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        super().__init__(pos, parent, brush, pen)
        self.elements: list[PathElement] = []

    ######## CLASSMETHODS ########

    @classmethod
    def straight_line(
        cls,
        start: PointDef,
        parent: Optional[Parent],
        stop: PointDef,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ) -> Path:
        """Convenience for drawing a single straight line.

        `stop` is measured relative to the starting point.
        """
        line = cls(start, parent, brush, pen)
        if isinstance(stop, tuple):
            stop = Point(*stop)
        line.line_to(stop.x, stop.y)
        return line

    @classmethod
    def rect(
        cls,
        pos: PointDef,
        parent: Optional[Parent],
        width: Unit,
        height: Unit,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
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
        parent: Optional[Parent],
        width: Unit,
        height: Unit,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """Convenience for drawing an ellipse.

        `pos` indicates the top left corner of the ellipse's bounding rect.
        To create a path from a center point, use `Path.ellipse_from_center`.

        This can also be used for drawing circles by giving the same width and height.
        """
        # Algorithm courtesy of https://stackoverflow.com/a/2173084/5615927
        path = cls(pos, parent, brush, pen)
        kappa = 0.5522848
        ox = (width / 2) * kappa  # control point offset horizontal
        oy = (height / 2) * kappa  # control point offset vertical
        xe = path.x + width  # x-end
        ye = path.y + height  # y-end
        xm = path.x + (width / 2)  # x-middle
        ym = path.y + (height / 2)  # y-middle
        path.move_to(path.x, ym)
        path.cubic_to(path.x, ym - oy, xm - ox, path.y, xm, path.y)
        path.cubic_to(xm + ox, path.y, xe, ym - oy, xe, ym)
        path.cubic_to(xe, ym + oy, xm + ox, ye, xm, ye)
        path.cubic_to(xm - ox, ye, path.x, ym + oy, path.x, ym)
        return path

    @classmethod
    def ellipse_from_center(
        cls,
        center_pos: PointDef,
        parent: Optional[Parent],
        width: Unit,
        height: Unit,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """Convenience for drawing an ellipse from its center point.

        See also `Path.ellipse`
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

    @staticmethod
    def _acute_arc_to_bezier(start: float, size: float) -> dict:
        """
        Generate a cubic Bezier representing an arc on the unit circle of total
        angle `size` radians, beginning `start` radians above the x-axis.
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
    def arc(
        cls,
        pos: PointDef,
        parent: Optional[Parent],
        width: Unit,
        height: Unit,
        start_angle: float,
        stop_angle: float,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
    ):
        """Convenience for drawing an elliptical arc.

        Args:
            pos: The position of the upper left corner of the traced ellipse.
            parent: The parent object or None
            width: The traced ellipse's width
            height: The traced ellipse's height
            start_angle: The starting arc angle in radians clockwise relative
                to the 3 o'clock position.
            stop_angle: The stopping arc angle in radians clockwise relative
                to the 3 o'clock position.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.

        The arc definition can be most easily understood as tracing an
        ellipse as defined in `Path.ellipse()`, where `pos` marks the
        top-left corner of the ellipse bounding rect. Two angles are
        provided in clockwise radians relative to the 3 o'clock
        position. The arc is traced from `start_angle` clockwise to
        `stop_angle`. Consequently, depending on the provided angles
        the actually drawn path may be far from the Path's position.

        The provided angles are interpreted mod `2*pi`. The angle
        between them must not be 0. This also means arc angles of
        `2*pi`, (i.e. complete ellipses), are not supported as they
        are interpreted as 0. Complete ellipses should instead be
        drawn with `Path.ellipse()`.

        Raises: ValueError: if invalid angles are given
        """
        # This method and `_acute_arc_to_bezier` are adapted from Joe
        # Cridge's algorithm and JS implementation found at
        # https://www.joecridge.me/bezier.pdf. Most of the original
        # comments have been left in place as well.

        # Work in float base units, converting back to units at the end
        TWO_PI = pi * 2
        HALF_PI = pi / 2

        w = width.base_value
        h = height.base_value

        # Make all angles positive...
        while start_angle < 0:
            start_angle += TWO_PI
        while stop_angle < 0:
            stop_angle += TWO_PI

        # ...and confine them to the interval [0,TWO_PI).
        start_angle %= TWO_PI
        stop_angle %= TWO_PI

        # Adjust angles to counter linear scaling.
        if start_angle <= HALF_PI:
            start_angle = atan(w / h * tan(start_angle))
        elif start_angle > HALF_PI and start_angle <= 3 * HALF_PI:
            start_angle = atan(w / h * tan(start_angle)) + pi
        else:
            start_angle = atan(w / h * tan(start_angle)) + TWO_PI
        if stop_angle <= HALF_PI:
            stop_angle = atan(w / h * tan(stop_angle))
        elif stop_angle > HALF_PI and stop_angle <= 3 * HALF_PI:
            stop_angle = atan(w / h * tan(stop_angle)) + pi
        else:
            stop_angle = atan(w / h * tan(stop_angle)) + TWO_PI

        # Exceed the interval if necessary in order to preserve the size and
        # orientation of the arc.
        if start_angle > stop_angle:
            stop_angle += TWO_PI

        # Create curves
        epsilon = 0.00001  # Smallest visible angle on displays up to 4K.
        arc_to_draw = 0.0
        curves = []
        while stop_angle - start_angle > epsilon:
            arc_to_draw = min(stop_angle - start_angle, HALF_PI)
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

    @classmethod
    def arrow(
        cls,
        start: PointDef,
        parent: Optional[Parent],
        end: PointDef,
        end_parent: Optional[Parent] = None,
        brush: Optional[SimpleBrushDef] = None,
        pen: Optional[SimplePenDef] = None,
        line_width: Unit = Mm(0.5),
        arrow_head_width: Unit = Mm(1),
        arrow_head_length: Unit = Mm(2),
    ) -> Path:
        """Convenience for drawing an arrow

        Args:
            start: The position of the center of the arrow line's start
            parent: A parent object
            end: The position of the arrow's tip, relative to `end_parent`
                if provided or `start`
            end_parent: An optional parent for the end point.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with. Defaults to no pen.
            line_width: The thickness of the arrow's line
            arrow_head_width: The width of the arrow head extending perpendicular
                from the line.
            arrow_head_length: The length of the arrow head parallel to the line.

        Note that `end_parent` is only used for initially drawing the
        path. If `end_parent` moves relative to the path after
        creation, the path shape will not be automatically updated.
        """
        # This algorithm is lightly adapted from
        # https://github.com/frogcat/canvas-arrow by Yuzo Matsuzawa
        # released under MIT.
        path = cls(start, parent, brush, pen or NO_PEN)
        end = Point.from_def(end)
        if end_parent:
            end = map_between(path, end_parent) + end
        # The original algorithm supports diverse shapes, including
        # things like double-headed arrows, using this system of a
        # variable numbers of control points. We don't use them right
        # now, but since we might want to later (and since I don't
        # understand the code enough to refactor it) it's left in
        # place here.
        control_points = [
            (0, line_width.base_value / 2),
            (-arrow_head_length.base_value, line_width.base_value / 2),
            (-arrow_head_length.base_value, arrow_head_width.base_value),
        ]
        # The start pos (relative to the path) is always (0, 0), so dx
        # and dy are just the end position
        dx = end.x.base_value
        dy = end.y.base_value
        length = sqrt(dx * dx + dy * dy)
        sin_ = dy / length
        cos_ = dx / length
        resolved_points: list[tuple[float, float]] = []
        resolved_points.append((0, 0))
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

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        """The breakable length of the path.

        This is calculated automatically from path contents. By extension,
        this means that by default all `Path` objects will automatically
        wrap in `Flowable`s.
        """
        # Find the positions of every path element relative to the path
        min_x = Unit(float("inf"))
        max_x = Unit(-float("inf"))
        for element in self.elements:
            # Determine element X relative to self
            relative_x = map_between_x(self, element)
            # Now update min/max accordingly
            if relative_x > max_x:
                max_x = relative_x
            if relative_x < min_x:
                min_x = relative_x
        return max_x - min_x

    ######## Public Methods ########

    def line_to(self, x: Unit, y: Unit, parent: Optional[Parent] = None):
        """Draw a path from the current position to a new point.

        A point parent may be passed as well, anchored the target
        point to a separate PositionedObject. In this case, the
        coordinates passed will be considered relative to the parent.

        If the path is empty, this will add two elements, an initial
        `MoveTo(Point(Unit(0), Unit(0)), self)` and the requested
        `LineTo`.

        Args:
            x: The end x position
            y: The end y position
            parent: An optional parent, whose position the target coordinate
                will be relative to.

        """
        if not len(self.elements):
            # Needed to ensure bounding rect / length calculations are correct
            self.elements.append(MoveTo(Point(Unit(0), Unit(0)), self))
        self.elements.append(LineTo(Point(x, y), parent or self))

    def move_to(self, x: Unit, y: Unit, parent: Optional[Parent] = None):
        """Close the current sub-path and start a new one.

        A point parent may be passed as well, anchored the target point to
        a separate `PositionedObject`. In this case, the coordinates passed will be
        considered relative to the parent.

        Args:
            x: The end x position
            y: The end y position
            parent: An optional parent, whose position the target coordinate will
                be relative to.
        """
        self.elements.append(MoveTo(Point(x, y), parent or self))

    def close_subpath(self):
        """Close the current sub-path and start a new one at the local origin.

        This is equivalent to `move_to(Unit(0), Unit(0))`

        Note:
            This convenience method does not support point parentage.
            If you need to anchor the new point, use an explicit
            `move_to(Unit(0), Unit(0), parent)` instead.
        """
        self.move_to(ZERO, ZERO)

    def cubic_to(
        self,
        control_1_x: Unit,
        control_1_y: Unit,
        control_2_x: Unit,
        control_2_y: Unit,
        end_x: Unit,
        end_y: Unit,
        control_1_parent: Optional[Parent] = None,
        control_2_parent: Optional[Parent] = None,
        end_parent: Optional[Parent] = None,
    ):
        """Draw a cubic bezier curve from the current position to a new point.

        If the path is empty, this will add two elements, an initial
        `MoveTo(Point(Unit(0), Unit(0)), self)` and the requested
        `CurveTo`.

        Args:
            control_1_x: The x coordinate of the first control point.
            control_1_y: The y coordinate of the first control point.
            control_2_x: The x coordinate of the second control point.
            control_2_y: The y coordinate of the second control point.
            end_x: The x coordinate of the curve target.
            end_y: The y coordinate of the curve target.
            control_1_parent: An optional parent for
                the first control point. Defaults to `self`.
            control_2_parent: An optional parent for
                the second control point. Defaults to `self`.
            end_parent: An optional parent for the
                curve target. Defaults to `self`.
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
            # Needed to ensure bounding rect / length calculations are correct
            self.elements.append(MoveTo(Point(Unit(0), Unit(0)), self))
        self.elements.append(CurveTo(Point(end_x, end_y), end_parent or self, c1, c2))

    def _relative_element_pos(self, element: Parent) -> Point:
        return map_between(self, element)

    def _resolve_path_elements(self) -> list[ResolvedPathElement]:
        resolved: list[ResolvedPathElement] = []
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
        clip_start_x: Optional[Unit] = None,
        clip_width: Optional[Unit] = None,
    ):
        # If this proves to be a performance bottleneck in the future,
        # it is very possible to optimize this to create `PathInterface`s
        # which reuse `QPainterPath`s.
        resolved_path_elements = self._resolve_path_elements()
        slice_interface = PathInterface(
            pos,
            self.brush.interface,
            self.pen.interface,
            resolved_path_elements,
            clip_start_x,
            clip_width,
        )
        slice_interface.render()
        self.interfaces.append(slice_interface)

    def _render_complete(
        self,
        pos: Point,
        dist_to_line_start: Optional[Unit] = None,
        local_start_x: Optional[Unit] = None,
    ):
        self._render_slice(pos, None, None)

    def _render_before_break(
        self, local_start_x: Unit, start: Point, stop: Point, dist_to_line_start: Unit
    ):
        self._render_slice(start, ZERO, stop.x - start.x)

    def _render_after_break(self, local_start_x: Unit, start: Point):
        self._render_slice(start, local_start_x, None)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        self._render_slice(start, local_start_x, stop.x - start.x)
