from typing import List, Optional, Union

from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import ZERO, Unit
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.multi_staff_object import MultiStaffObject
from neoscore.western.staff_group import StaffGroup


class SystemLine(MultiStaffObject, MusicPath):

    """A line connecting staves at the beginning of every system.

    This is drawn in the fringe of every staff system in the specified group.
    """

    def __init__(
        self,
        staves: Union[StaffGroup, List[AbstractStaff]],
        font: Optional[MusicFont] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            staves: The staves spanned. If a raw list of staves is given, it must be
                in descending order.
            font: If provided, this overrides the font in the parent (top) staff.
            pen: An override to the pen normally derived from the active music font.
        """
        MultiStaffObject.__init__(self, staves)
        font = font or self.highest.music_font
        if pen is None:
            pen = Pen(thickness=font.engraving_defaults["staffLineThickness"])
        MusicPath.__init__(self, ORIGIN, self.highest, font, pen=pen)
        self.move_to(ZERO, self.highest.barline_extent[0])
        self.line_to(ZERO, self.map_to(self.lowest).y + self.lowest.barline_extent[1])

    @property
    def breakable_length(self) -> Unit:
        """This class's breakable length is that of its highest staff"""
        return self.highest.breakable_length

    def _render_occurrence(
        self,
        pos: Point,
        flowable_line: Optional[NewLine],
    ):
        fringe_layout = self.highest.fringe_layout_at(flowable_line)
        super().render_complete(
            Point(pos.x + fringe_layout.staff, pos.y), flowable_line
        )

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        self._render_occurrence(pos, flowable_line)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        self._render_occurrence(pos, flowable_line)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        self._render_occurrence(pos, flowable_line)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        self._render_occurrence(pos, flowable_line)
