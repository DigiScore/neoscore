from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from neoscore.core import neoscore
from neoscore.core.layout_controller import LayoutController
from neoscore.core.mapping import canvas_pos_of
from neoscore.core.new_line import NewLine
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.exceptions import OutOfBoundsError
from neoscore.utils.point import Point, PointDef
from neoscore.utils.units import ZERO, Mm, Unit

if TYPE_CHECKING:
    from neoscore.core.mapping import Parent


class Flowable(PositionedObject):

    """A flowable coordinate space container.

    This provides a virtual horizontal strip of space in which
    objects can be placed, and at render time be automatically
    flowed across line breaks and page breaks in the document.

    To place an object in a `Flowable`, simply parent it
    to one, or to an object already in one.

    In typical scores, there will be a single `Flowable`
    placed in the first page of the document, and the vast
    majority of objects will be placed inside it.
    """

    _neoscore_flowable_type_marker = True

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[Parent],
        width: Unit,
        height: Unit,
        y_padding: Unit = Mm(5),
        break_threshold: Unit = Mm(5),
    ):
        """
        Args:
            pos: Starting position in relative to the top left corner of the
                live document area of the first page
            parent: An optional parent object. Nested flowables are not supported,
                so this should not be a flowable or in one. This defaults to the
                document's first page.
            width: length of the flowable
            height: height of the flowable
            y_padding: The vertical gap between flowable sections
            break_threshold: The maximum distance the flowable will shorten a line
                to allow a break to occur on a `BreakOpportunity`
        """
        super().__init__(pos, parent)
        self._length = width
        self._height = height
        self._y_padding = y_padding
        self._break_threshold = break_threshold
        self._layout_controllers = self._generate_layout_controllers()

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self) -> Unit:
        """The length of the unwrapped flowable"""
        return self._length

    @property
    def height(self) -> Unit:
        """The height of the unwrapped flowable"""
        return self._height

    @height.setter
    def height(self, value: Unit):
        self._height = value

    @property
    def y_padding(self) -> Unit:
        """The padding between wrapped sections of the flowable"""
        return self._y_padding

    @y_padding.setter
    def y_padding(self, value: Unit):
        self._y_padding = value

    @property
    def break_threshold(self) -> Unit:
        """The threshold for `BreakOpportunity`-aware line breaks.

        This is the maximum distance the flowable will shorten a line to allow
        a break to occur on a `BreakOpportunity`.

        If set to `Unit(0)` (or in an equivalent unit), `BreakOpportunity`s
        will be entirely ignored during layout.
        """
        return self._break_threshold

    @break_threshold.setter
    def break_threshold(self, value: Unit):
        self._break_threshold = value

    @property
    def layout_controllers(self) -> list[LayoutController]:
        """Controllers affecting flowable layout"""
        return self._layout_controllers

    @layout_controllers.setter
    def layout_controllers(self, value: list[LayoutController]):
        self._layout_controllers = value

    def _generate_layout_controllers(self) -> list[NewLine]:
        """Generate automatic layout controllers.

        The generated controllers are stored in `self.layout_controllers`
        in sorted order according to ascending x position
        """
        live_page_width = neoscore.document.paper.live_width
        live_page_height = neoscore.document.paper.live_height
        # local progress of layout generation; when the entire flowable has
        # been covered, this will be equal to `self.width`
        x_progress = ZERO
        # Current position on the page relative to the top left corner
        # of the live page area
        pos_x = self.pos.x
        pos_y = self.pos.y
        current_page = 0
        # Attach initial line controller
        layout_controllers = [
            NewLine(
                self.pos, neoscore.document.pages[current_page], x_progress, self.height
            )
        ]
        while True:
            x_progress += live_page_width - pos_x
            pos_y = pos_y + self.height + self.y_padding
            if x_progress >= self.length:
                # End of breakable width - Done.
                break
            if pos_y > live_page_height:
                # Page break - No y offset
                pos_x = ZERO
                pos_y = ZERO
                current_page += 1
                layout_controllers.append(
                    NewLine(
                        Point(pos_x, pos_y),
                        neoscore.document.pages[current_page],
                        x_progress,
                        self.height,
                    )
                )
            else:
                # Line break - self.y_padding as y offset
                pos_x = ZERO
                layout_controllers.append(
                    NewLine(
                        Point(pos_x, pos_y),
                        neoscore.document.pages[current_page],
                        x_progress,
                        self.height,
                        self.y_padding,
                    )
                )
        return layout_controllers

    def map_to_canvas(self, local_point: Point) -> Point:
        """Convert a local point to its position in the canvas.

        Args:
            local_point: A position in the flowable's local space.
        """
        line = self.last_break_at(local_point.x)
        line_canvas_pos = canvas_pos_of(line)
        return line_canvas_pos + Point(local_point.x - line.flowable_x, local_point.y)

    def dist_to_line_start(self, flowable_x: Unit) -> Unit:
        """Find the distance of an x-pos to the left edge of its laid-out line.

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        line_start = self.last_break_at(flowable_x)
        return flowable_x - line_start.flowable_x

    def dist_to_line_end(self, flowable_x: Unit) -> Unit:
        """Find the distance of an x-pos to the right edge of its laid-out line.

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        return self.dist_to_line_start(flowable_x) - neoscore.document.paper.live_width

    def last_break_at(self, flowable_x: Unit) -> NewLine:
        """Find the last `NewLine` that occurred before a given local flowable_x-pos

        The result of this function will be accurate within `Unit(1)`

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        return self.layout_controllers[self.last_break_index_at(flowable_x)]

    def last_break_index_at(self, flowable_x: Unit) -> int:
        """Like `last_break_at`, but returns an index.

        The result of this function will be accurate within `Unit(1)`

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        # Note that this assumes that all layout controllers are line
        # breaks, and will not work if/when other types are added
        remaining_x = flowable_x
        for i, controller in enumerate(self.layout_controllers):
            remaining_x -= controller.length
            # Allow error of Unit(1) to compensate for repeated subtraction
            # rounding errors.
            if remaining_x.base_value < -1:
                return i
        else:
            raise OutOfBoundsError(
                "flowable_x={} lies outside of this Flowable".format(flowable_x)
            )
