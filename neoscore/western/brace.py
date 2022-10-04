from typing import List, Optional, Union, cast

from neoscore.core.brush import BrushDef
from neoscore.core.layout_controllers import MarginController, NewLine
from neoscore.core.music_font import MusicFont, MusicFontGlyphNotFoundError
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import Point
from neoscore.core.text_alignment import AlignmentX
from neoscore.core.units import ZERO, Unit
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.multi_staff_object import MultiStaffObject
from neoscore.western.staff_group import StaffGroup


class Brace(MultiStaffObject, MusicText):

    """A brace spanning staves.

    This is drawn in the fringe of every staff system in the specified group.
    """

    def __init__(
        self,
        staves: Union[StaffGroup, List[AbstractStaff]],
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            staves: The staves spanned. If a raw list of staves is given, it must be
                in descending order.
            font: If provided, this overrides the font in the parent (top) staff.
            brush: The brush to fill shapes with.
            pen: The pen to draw outlines with.
        """
        MultiStaffObject.__init__(self, staves)
        # Calculate the height of the brace in highest_staff staff units
        scale = cast(float, self.vertical_span / self.highest.unit(4))
        if self.vertical_span > self.highest.unit(50):
            text = ("brace", 4)
        elif self.vertical_span > self.highest.unit(30):
            text = ("brace", 3)
        elif self.vertical_span > self.highest.unit(15):
            text = ("brace", 2)
        elif self.vertical_span > self.highest.unit(4):
            text = "brace"
        else:
            text = ("brace", 1)
        try:
            # Attempt to use size-specific optional glyph
            MusicText.__init__(
                self,
                (ZERO, self.vertical_span),
                self.highest,
                text,
                font,
                brush,
                pen,
                scale,
                alignment_x=AlignmentX.RIGHT,
            )
        except MusicFontGlyphNotFoundError:
            # Default to non-optional glyph
            MusicText.__init__(
                self,
                (ZERO, self.vertical_span),
                self.highest,
                "brace",
                font,
                brush,
                pen,
                scale,
                alignment_x=AlignmentX.RIGHT,
            )

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

    def _register_layout_controllers(self):
        flowable = self.flowable
        if not flowable:
            return
        staff_flowable_x = flowable.descendant_pos_x(self.highest)
        flowable.add_margin_controller(
            MarginController(
                staff_flowable_x,
                self.bounding_rect.width,
                "_neoscore_brace",
            )
        )

    def pre_render_hook(self):
        super().pre_render_hook()
        self._register_layout_controllers()
