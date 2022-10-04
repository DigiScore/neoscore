from __future__ import annotations

from typing import Optional

from sortedcontainers import SortedKeyList

from neoscore.core import neoscore
from neoscore.core.layout_controllers import MarginController, NewLine
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit


class Flowable(PositionedObject):

    """A flowable coordinate space container.

    This provides a virtual horizontal strip of space in which objects can be placed,
    and at render time be automatically flowed across line breaks and page breaks in the
    document.

    To place an object in a ``Flowable``, simply parent it to one, or to an object
    already in one.

    In typical scores, there will be a single ``Flowable`` placed in the first page of
    the document, and most objects will be placed inside it.
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
        self._lines = []
        self._provided_controllers = Flowable._new_provided_controllers_list()

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
        """The threshold for :obj:`.BreakOpportunity`-aware line breaks.

        This is the maximum distance the flowable will shorten a line to allow
        a break to occur on a ``BreakOpportunity``.

        If set to ``ZERO``, break opportunities will be entirely ignored during
        layout. On the other hand, if set to a value larger than the live page width,
        all break opportunities will be taken.
        """
        return self._break_threshold

    @break_threshold.setter
    def break_threshold(self, value: Unit):
        self._break_threshold = value

    @property
    def lines(self) -> List[NewLine]:
        """The generated lines of this flowable.

        This property is managed and should not be modified."""
        return self._lines

    @lines.setter
    def lines(self, value: List[NewLine]):
        self._lines = value

    @property
    def provided_controllers(self) -> SortedKeyList[MarginController]:
        """Layout controllers provided by users.

        Currently, this only supports margin controllers. Eventually on we may expand
        this to allow things like explicit user-defined ``NewLine``\ s.

        Controllers should not be added directly to this list; use
        :obj:`.add_margin_controller` instead.
        """
        return self._provided_controllers

    def add_margin_controller(self, controller: MarginController):
        """Add a margin controller if applicable.

        If ``provided_controllers`` already has a margin controller at the given
        ``controller.flowable_x`` with the same ``layer_key``, the controller is only
        inserted if its margin is larger than the existing one.
        """
        if not self._provided_controllers:
            self._provided_controllers.add(controller)
            return
        idx = self._provided_controllers.bisect_left(controller)

        for i in range(idx, len(self._provided_controllers)):
            existing_controller = self._provided_controllers[i]
            if existing_controller.flowable_x > controller.flowable_x:
                # No existing controllers at this flowable_x and layer found
                break
            if existing_controller.layer_key == controller.layer_key:
                # Existing controller at this flowable_x and layer found
                if existing_controller.margin_left >= controller.margin_left:
                    # Existing controller margin is larger than one being added; skip it
                    return
                else:
                    # Existing controller margin is smaller than one being added; replace it
                    self._provided_controllers.pop(i)
                    break
        self._provided_controllers.add(controller)

    def _generate_lines(self):
        """Generate automatic layout controllers.

        The generated controllers are stored in ``self.layout_controllers``
        in sorted order by ascending x position
        """
        live_page_width = neoscore.document.paper.live_width
        live_page_height = neoscore.document.paper.live_height
        break_opps = self._find_break_opportunities()
        for c in self.lines:
            c.remove()
        self.lines = []
        while True:
            if not self.lines:
                flowable_start_x = ZERO
                page = self.first_ancestor_with_attr("_neoscore_page_type_marker")
                flowable_page_pos = page.map_to(self)
                new_line_x = flowable_page_pos.x + self._active_margin_at(
                    flowable_start_x
                )
                new_line_y = flowable_page_pos.y
            else:
                last = self.lines[-1]
                flowable_start_x = last.flowable_x + last.length
                page = last.page
                new_line_x = self._active_margin_at(flowable_start_x)
                new_line_y = last.y + self.height + self.y_padding
                new_line_bottom_y = new_line_y + self.height
                if (
                    new_line_y > live_page_height
                    or new_line_bottom_y > live_page_height
                ):
                    page = neoscore.document.pages[page.index + 1]
                    new_line_y = ZERO
            # Now determine this line's length
            max_length = live_page_width - new_line_x
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
            self.lines.append(
                NewLine(
                    (new_line_x, new_line_y),
                    page,
                    flowable_start_x,
                    length,
                    self.height,
                )
            )
            if flowable_start_x + length > self.length:
                break

    def _find_break_opportunities(self) -> List[Unit]:
        """Find the relative X positions of every break hint in this flowable.

        The returned positions will be sorted.
        """
        opps = self.descendants_with_attribute(
            "_neoscore_break_opportunity_type_marker"
        )
        return sorted((self.map_x_to(opp) for opp in opps))

    def _active_margin_at(self, flowable_x: Unit) -> Unit:
        active_margin_layers: Dict[str, Unit] = {}
        for controller in self.provided_controllers:
            if controller.flowable_x > flowable_x:
                break
            active_margin_layers[controller.layer_key] = controller.margin_left
        return sum(active_margin_layers.values(), ZERO)

    def map_to_canvas(self, local_point: Point) -> Point:
        """Convert a local point to its position in the canvas.

        Note that this should only be called at render-time, since it depends on layout
        controllers only generated once the flowable has started rendering.

        Args:
            local_point: A position in the flowable's local space.
        """
        if not getattr(self, "_currently_rendering", None):
            print("WARNING: Called Flowable.map_to_canvas outside rendering context")
        line = self.last_break_at(local_point.x)
        line_canvas_pos = line.canvas_pos()
        return line_canvas_pos + Point(local_point.x - line.flowable_x, local_point.y)

    def last_break_at(self, flowable_x: Unit) -> NewLine:
        """Find the last ``NewLine`` that occurred before a given local flowable_x-pos

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        return self.lines[self.last_break_index_at(flowable_x)]

    def last_break_index_at(self, flowable_x: Unit) -> int:
        """Like ``last_break_at``, but returns an index.

        Args:
            flowable_x: An x-axis location in the virtual flowable space.
        """
        # Note that this assumes that all layout controllers are line
        # breaks, and will not work if/when other types are added
        remaining_x = flowable_x
        for i, controller in enumerate(self.lines):
            remaining_x -= controller.length
            if remaining_x <= ZERO:
                return i
        else:
            return len(self.lines) - 1

    def render(self):
        super().render()

    def pre_render_hook(self):
        super().pre_render_hook()
        self._generate_lines()

    def post_render_hook(self):
        # Clear all auto-generated margin controllers
        super().post_render_hook()
        self._provided_controllers = Flowable._new_provided_controllers_list()

    @staticmethod
    def _new_provided_controllers_list() -> SortedKeyList[MarginController]:
        return SortedKeyList(key=lambda c: c.flowable_x)
