from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from brown import constants
from brown.core.brush import Brush, SimpleBrushDef
from brown.core.graphic_object import GraphicObject
from brown.core.mapping import map_between, map_between_x
from brown.core.path_element import ControlPoint, CurveTo, LineTo, MoveTo, PathElement
from brown.core.pen import SimplePenDef
from brown.interface.path_interface import (
    PathInterface,
    ResolvedCurveTo,
    ResolvedLineTo,
    ResolvedMoveTo,
    ResolvedPathElement,
)
from brown.utils.point import Point, PointDef
from brown.utils.units import ZERO, Unit

if TYPE_CHECKING:
    from brown.core.mapping import Parent


class Path(GraphicObject):

    """A vector path whose points can be anchored to other objects.

    If a Path is in a `Flowable`, any point anchors in the path
    should be anchored to objects in the same `Flowable`, or
    undefined behavior may occur. Likewise, if a Path is not
    in a `Flowable`, all point anchors should not be in one either.
    """

    _default_brush = Brush(
        constants.DEFAULT_PATH_BRUSH_COLOR, constants.DEFAULT_BRUSH_PATTERN
    )

    def __init__(
        self,
        pos: PointDef,
        pen: Optional[SimplePenDef] = None,
        brush: Optional[SimpleBrushDef] = None,
        parent: Optional[Parent] = None,
    ):
        """
        Args:
            pos: The position of the path root.
            pen: The pen to draw outlines with.
            brush: The brush to draw outlines with.
            parent: The parent object or None
        """
        brush = brush or Brush.from_existing(Path._default_brush)
        super().__init__(pos, ZERO, pen, brush, parent)
        self.elements: list[PathElement] = []

    ######## CLASSMETHODS ########

    @classmethod
    def straight_line(
        cls,
        start: PointDef,
        stop: PointDef,
        pen: Optional[SimplePenDef] = None,
        brush: Optional[SimpleBrushDef] = None,
        parent: Parent = None,
    ) -> Path:
        """Path: Constructor for a straight line

        Args:
            start: Starting position relative to the parent
            stop: Ending position relative to the parent.
            pen: The pen to draw outlines with.
            brush: The brush to draw outlines with.
            parent: The parent object or None
        """
        line = cls(start, pen, brush, parent)
        if isinstance(stop, tuple):
            stop = Point(*stop)
        line.line_to(stop.x, stop.y)
        return line

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

        A point parent may be passed as well, anchored the target point to
        a separate GraphicObject. In this case, the coordinates passed will be
        considered relative to the parent.

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
        a separate `GraphicObject`. In this case, the coordinates passed will be
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
        self.elements.append(CurveTo(c1, c2, Point(end_x, end_y), end_parent or self))

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
            self.pen.interface,
            self.brush.interface,
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

    def _render_after_break(self, local_start_x: Unit, start: Point, stop: Point):
        self._render_slice(start, local_start_x, stop.x - start.x)

    def _render_spanning_continuation(
        self, local_start_x: Unit, start: Point, stop: Point
    ):
        self._render_slice(start, local_start_x, stop.x - start.x)
