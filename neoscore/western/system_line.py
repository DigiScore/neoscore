from typing import Optional

from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen, PenDef
from neoscore.core.point import Point
from neoscore.core.units import ZERO, Unit
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.multi_staff_object import MultiStaffObject


class SystemLine(MultiStaffObject, MusicPath):

    """A line connecting staves at the beginning of every system.

    The line is drawn at the beginning of every line starting at the line containing
    its initial x position until the end of the staff.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: list[AbstractStaff],
        font: Optional[MusicFont] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos_x: The starting X position relative to the highest staff.
            staves: The staves spanned. Must be in visually descending order.
            font: If provided, this overrides the font in the parent (top) staff.
            pen: An override to the pen normally derived from the active music font.
        """
        MultiStaffObject.__init__(self, staves)
        font = font or self.highest.music_font
        if pen is None:
            pen = Pen(thickness=font.engraving_defaults["staffLineThickness"])
        MusicPath.__init__(self, (pos_x, ZERO), self.highest, font, pen=pen)
        self.move_to(ZERO, self.highest.barline_extent[0])
        self.line_to(ZERO, self.map_to(self.lowest).y + self.lowest.barline_extent[1])

    @property
    def breakable_length(self) -> Unit:
        """The breakable length of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self.parent.breakable_length - self.x

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        fringe_layout = self.highest.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.staff, pos.y))

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        fringe_layout = self.highest.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.staff, pos.y))

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        fringe_layout = self.highest.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.staff, pos.y))

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        fringe_layout = self.highest.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.staff, pos.y))
