from __future__ import annotations

from typing import Any, List, Optional, Tuple

from neoscore.core.has_music_font import HasMusicFont
from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.painted_object import PaintedObject
from neoscore.core.path import Path
from neoscore.core.pen import PenDef
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Unit
from neoscore.western.staff_fringe_layout import StaffFringeLayout
from neoscore.western.staff_group import StaffGroup


class AbstractStaff(PaintedObject, HasMusicFont):
    """An abstract superclass for staves.

    This is not meant to be used directly."""

    # Type sentinel used to hackily check if objects are Staff
    # without importing the type, risking cyclic imports.
    _neoscore_abstract_staff_type_marker = True

    def __init__(
        self,
        pos: PointDef,
        parent: Optional[PositionedObject],
        length: Unit,
        group: Optional[StaffGroup],
        line_spacing: Unit,
        line_count: int,
        music_font: Optional[MusicFont],
        pen: Optional[PenDef],
    ):
        self._music_font = music_font
        PaintedObject.__init__(self, pos, parent, pen=pen)
        self._line_spacing = line_spacing
        self._line_count = line_count
        self._length = length
        self._group = group or StaffGroup()
        self._group.staves.add(self)

    @property
    def music_font(self) -> MusicFont:
        return self._music_font

    @property
    def height(self) -> Unit:
        """The height of the staff from top to bottom line.

        If the staff only has one line, its height is defined as 0.
        """
        return self.line_spacing * (self.line_count - 1)

    @property
    def line_spacing(self) -> Unit:
        """The distance between two lines in the staff."""
        return self._line_spacing

    @property
    def line_count(self) -> int:
        """The number of lines in the staff"""
        return self._line_count

    @property
    def center_y(self) -> Unit:
        """The position of the center staff position"""
        return self.height / 2

    @property
    def barline_extent(self) -> Tuple[Unit, Unit]:
        """The starting and stopping Y positions of barlines in this staff.

        For staves with more than 1 line, this extends from the top line to bottom
        line. For single-line staves, this extends from 1 unit above and below the
        staff.
        """
        if self.line_count == 1:
            return -self.line_spacing, self.line_spacing
        else:
            return ZERO, self.height

    @property
    def breakable_length(self) -> Unit:
        """Staves are breakable over their full length"""
        # Override expensive ``Path.length`` since the staff length here
        # is already known.
        return self._length

    @property
    def group(self) -> StaffGroup:
        """The staff group this belongs to.

        A staff group should be assigned during initalization for proper display of
        staff systems.
        """
        return self._group

    def find_ordered_descendants_with_attr(self, attr: str) -> List[Tuple[Unit, Any]]:
        """Find all descendants with an attribute, sorted with their staff x positions"""
        result = [
            (self.descendant_pos_x(obj), obj)
            for obj in self.descendants_with_attribute(attr)
        ]
        result.sort(key=lambda tup: tup[0])
        return result

    def y_inside_staff(self, pos_y: Unit) -> bool:
        """Determine if a y-axis position is inside the staff.

        This is true for any position within or on the outer lines.
        """
        return ZERO <= pos_y <= self.height

    def fringe_layout_at(self, location: Optional[NewLine]) -> StaffFringeLayout:
        return self.group.fringe_layout_at(self, location)

    def _render_slice(
        self,
        pos: Point,
        clip_start_x: Optional[Unit],
        clip_width: Optional[Unit],
        flowable_line: Optional[NewLine],
    ):
        fringe_layout = self.fringe_layout_at(flowable_line)
        if clip_width is None:
            if clip_start_x is None:
                slice_length = self.breakable_length
            else:
                slice_length = self.breakable_length - clip_start_x
        else:
            slice_length = clip_width
        inside_flowable = bool(flowable_line)
        if inside_flowable:
            segment_pos = Point(pos.x + fringe_layout.staff, pos.y)
        else:
            segment_pos = Point(fringe_layout.staff, ZERO)
        path = self._create_staff_segment_path(
            segment_pos, slice_length - fringe_layout.staff, inside_flowable
        )
        path.render()
        path.remove()

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        self._render_slice(pos, None, None, flowable_line)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        self._render_slice(
            pos,
            ZERO,
            flowable_line.flowable_x + flowable_line.length - flowable_x,
            flowable_line,
        )

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        self._render_slice(pos, object_x, flowable_line.length, flowable_line)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        self._render_slice(pos, object_x, None, flowable_line)

    def _create_staff_segment_path(
        self, pos: Point, length: Unit, inside_flowable: bool
    ) -> Path:
        parent = None if inside_flowable else self
        path = Path(pos, parent, pen=self.pen)
        line_y = ZERO
        for i in range(self.line_count):
            path.move_to(ZERO, line_y)
            path.line_to(length, line_y)
            line_y += self.line_spacing
        return path

    def register_layout_controllers(self):
        """Register any flowable margin controllers needed by the staff.

        Staff subclasses must implement this.
        """
        raise NotImplementedError

    def fringe_layout_for_isolated_staff(
        self, location: Optional[NewLine]
    ) -> StaffFringeLayout:
        """Determine the staff fringe layout of this staff in isolation.

        This is the layout needed if this staff was alone in a staff system.
        ``StaffGroup`` uses this as a starting point in its fringe layout logic.

        Staff subclasses must implement this.
        """
        raise NotImplementedError

    def pre_render_hook(self):
        super().pre_render_hook()
        self.register_layout_controllers()
