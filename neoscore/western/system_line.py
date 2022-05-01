from typing import Optional

from neoscore.core.mapping import map_between
from neoscore.core.music_font import MusicFont
from neoscore.core.music_path import MusicPath
from neoscore.core.pen import Pen, PenDef
from neoscore.core.units import ZERO, Unit
from neoscore.western.multi_staff_object import MultiStaffObject, StaffLike


class SystemLine(MultiStaffObject, MusicPath):

    """A line connecting staves at the beginning of every system.

    The line is drawn at the beginning of every line starting at the line containing
    its initial x position until the end of the staff.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: list[StaffLike],
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
        self.line_to(
            ZERO, map_between(self, self.lowest).y + self.lowest.barline_extent[1]
        )

    @property
    def breakable_length(self) -> Unit:
        """The breakable length of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self.parent.breakable_length - self.x

    def render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        self.render_complete(start)

    def render_after_break(self, local_start_x, start):
        self.render_complete(start)

    def render_spanning_continuation(self, local_start_x, start, stop):
        self.render_complete(start)
