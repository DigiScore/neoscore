from __future__ import annotations

from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import BrushDef
from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import Point
from neoscore.core.text_alignment import AlignmentY
from neoscore.core.units import ZERO, Unit
from neoscore.western.staff_object import StaffObject
from neoscore.western.tab_staff import TabStaff


class TabClef(MusicText, StaffObject):

    """A tablature clef.

    Unlike classical :obj:`.Clef`\ s, this is purely cosmetic. It must be placed in a
    :obj:`.TabStaff`, and it is automatically positioned at its beginning. If the
    ``TabStaff`` is in a flowable, this automatically repeats at the beginning of every
    flowed staff line for the length of the staff. Because clef changes are generally
    inapplicable to tabs, clef changes are not currently supported.
    """

    # Type sentinel used to hackily check type
    # without importing the type, risking cyclic imports.
    _neoscore_tab_clef_type_marker = True

    def __init__(
        self,
        staff: TabStaff,
        glyph_name: str = "6stringTabClef",
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
        hide_background: bool = True,
    ):
        """
        Args:
            staff: The parent staff
            glyph_name: The SMuFL glyph to use.
            font: The font to use. Defaults to the staff's font.
            brush: The brush to fill in text shapes with.
            pen: The pen to trace text outlines with. This defaults to no pen.
            hide_background: Whether to paint over the background behind the text.
        """
        StaffObject.__init__(self, staff)
        MusicText.__init__(
            self,
            (ZERO, staff.center_y),
            staff,
            glyph_name,
            font,
            brush,
            pen,
            background_brush=neoscore.background_brush if hide_background else None,
            alignment_y=AlignmentY.CENTER,
        )

    @property
    def breakable_length(self) -> Unit:
        """Tab clefs are drawn at the beginning of every line in a staff."""
        return self.parent.breakable_length - self.x

    def render_complete(
        self,
        pos: Point,
        flowable_line: Optional[NewLine] = None,
        flowable_x: Optional[Unit] = None,
    ):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        if fringe_layout.pos_x_in_staff == self.pos_x_in_staff:
            pos = Point(pos.x + fringe_layout.clef, pos.y)
        super().render_complete(pos, flowable_line, flowable_x)

    def render_before_break(self, pos: Point, flowable_line: NewLine, flowable_x: Unit):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        if fringe_layout.pos_x_in_staff == self.pos_x_in_staff:
            pos = Point(pos.x + fringe_layout.clef, pos.y)
        super().render_complete(pos, flowable_line)

    def render_spanning_continuation(
        self, pos: Point, flowable_line: NewLine, object_x: Unit
    ):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.clef, pos.y), flowable_line)

    def render_after_break(self, pos: Point, flowable_line: NewLine, object_x: Unit):
        fringe_layout = self.staff.fringe_layout_at(flowable_line)
        super().render_complete(Point(pos.x + fringe_layout.clef, pos.y), flowable_line)
