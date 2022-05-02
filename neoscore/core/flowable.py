from __future__ import annotations

from typing import Optional

from neoscore.core import neoscore
from neoscore.core.layout_controller import LayoutController
from neoscore.core.new_line import NewLine
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit


class Flowable(PositionedObject):

    """A flowable coordinate space container.

    This provides a virtual horizontal strip of space in which
    objects can be placed, and at render time be automatically
    flowed across line breaks and page breaks in the document.

    To place an object in a ``Flowable``, simply parent it
    to one, or to an object already in one.

    In typical scores, there will be a single ``Flowable``
    placed in the first page of the document, and most objects
    will be placed inside it.
    """

    _neoscore_flowable_type_marker = True

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        length: Unit,
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
            length: length of the flowable
            height: height of the flowable
            y_padding: The vertical gap between flowable sections
            break_threshold: The maximum distance the flowable will shorten a line
                to allow a break to occur on a ``BreakOpportunity``
        """
        super().__init__(pos, parent)
        self._length = length
        self._height = height
        self._y_padding = y_padding
        self._break_threshold = break_threshold
        self._layout_controllers = []

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
        """The threshold for ``BreakOpportunity``-aware line breaks.

        This is the maximum distance the flowable will shorten a line to allow
        a break to occur on a ``BreakOpportunity``.

        If set to ``ZERO``, ``BreakOpportunity``\ s will be entirely ignored during
        layout. On the other hand, if set to a value larger than the live page width,
        all break opportunities will be taken.
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

    def _generate_layout_controllers(self):
        """Generate automatic layout controllers.

        The generated controllers are stored in ``self.layout_controllers``
        in sorted order according to ascending x position
        """
        live_page_width = neoscore.document.paper.live_width
        live_page_height = neoscore.document.paper.live_height
        break_opps = self._find_break_opportunities()
        for c in self.layout_controllers:
            c.remove()
        self.layout_controllers = []
        while True:
            if not self.layout_controllers:
                flowable_start_x = ZERO
                page = self.first_ancestor_with_attr("_neoscore_page_type_marker")
                flowable_page_pos = page.map_to(self)
                controller_x = flowable_page_pos.x
                controller_y = flowable_page_pos.y
            else:
                last = self.layout_controllers[-1]
                flowable_start_x = last.flowable_x + last.length
                page = last.page
                controller_x = ZERO
                controller_y = last.y + self.height + self.y_padding
                controller_bottom_y = controller_y + self.height
                if (
                    controller_y > live_page_height
                    or controller_bottom_y > live_page_height
                ):
                    page = neoscore.document.pages[page.page_index + 1]
                    controller_y = ZERO
            # Now determine this line's length
            max_length = live_page_width - controller_x
            max_line_end_flowable_x = flowable_start_x + max_length
            nearest_break_opp = next(
                (opp for opp in reversed(break_opps) if opp < max_line_end_flowable_x),
                None,
            )
            if (
                nearest_break_opp
                and max_line_end_flowable_x - nearest_break_opp < self.break_threshold
            ):
                length = nearest_break_opp - flowable_start_x
            else:
                length = max_length
            self.layout_controllers.append(
                NewLine(
                    (controller_x, controller_y),
                    page,
                    flowable_start_x,
                    length,
                    self.height,
                )
            )
            if flowable_start_x + length > self.length:
                break

    def _find_break_opportunities(self) -> list[Unit]:
        """Find the relative X positions of every break hint in this flowable.

        The returned positions will be sorted.
        """
        opps = self.descendants_with_attribute(
            "_neoscore_break_opportunity_type_marker"
        )
        return sorted((self.map_x_to(opp) for opp in opps))

    def map_to_canvas(self, local_point: Point) -> Point:
        """Convert a local point to its position in the canvas.

        Note that this should only be called at render-time, since it depends on layout
        controllers only generated once the flowable has started rendering.

        Args:
            local_point: A position in the flowable's local space.
        """
        line = self.last_break_at(local_point.x)
        line_canvas_pos = line.canvas_pos
        return line_canvas_pos + Point(local_point.x - line.flowable_x, local_point.y)

    def dist_to_line_start(self, flowable_x: Unit) -> Unit:
        """Find the distance of an x-pos to the left edge of its laid-out line.

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        line = self.last_break_at(flowable_x)
        return flowable_x - line.flowable_x

    def dist_to_line_end(self, flowable_x: Unit) -> Unit:
        """Find the distance of an x-pos to the right edge of its laid-out line.

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        line = self.last_break_at(flowable_x)
        return (line.flowable_x + line.length) - flowable_x

    def last_break_at(self, flowable_x: Unit) -> NewLine:
        """Find the last ``NewLine`` that occurred before a given local flowable_x-pos

        The result of this function will be accurate within ``Unit(1)``

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        return self.layout_controllers[self.last_break_index_at(flowable_x)]

    # TODO HIGH Maybe provide an "affinity" switch with objects to state how they should be drawn when they lie almost exactly at a break - could render in first break, second break, or both. current behavior is to only return the second i think, which causes weird behavior with things like barlines.

    def last_break_index_at(self, flowable_x: Unit) -> int:
        """Like ``last_break_at``, but returns an index.

        The result of this function will be accurate within ``Unit(1)``

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        # Note that this assumes that all layout controllers are line
        # breaks, and will not work if/when other types are added
        remaining_x = flowable_x
        for i, controller in enumerate(self.layout_controllers):
            remaining_x -= controller.length
            if remaining_x.base_value < 0:
                return i
        else:
            return len(self.layout_controllers) - 1

    def render(self):
        self._generate_layout_controllers()
        super().render()
