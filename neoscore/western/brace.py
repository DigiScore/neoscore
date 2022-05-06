from typing import Optional, cast

from neoscore.core.brush import BrushDef
from neoscore.core.layout_controllers import NewLine
from neoscore.core.music_font import MusicFont, MusicFontGlyphNotFoundError
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import Point
from neoscore.core.text_alignment import AlignmentX
from neoscore.core.units import Unit
from neoscore.western.abstract_staff import AbstractStaff
from neoscore.western.multi_staff_object import MultiStaffObject


class Brace(MultiStaffObject, MusicText):

    """A brace spanning staves, recurring at line beginnings.

    The brace is drawn at the beginning of every line starting at the line containing
    its initial x position until the end of the staff.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: list[AbstractStaff],
        font: Optional[MusicFont] = None,
        brush: Optional[BrushDef] = None,
        pen: Optional[PenDef] = None,
    ):
        """
        Args:
            pos_x: The starting X position relative to the highest staff.
            staves: The staves spanned. Must be in visually descending order.
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
                (pos_x, self.vertical_span),
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
                (pos_x, self.vertical_span),
                self.highest,
                "brace",
                font,
                brush,
                pen,
                scale,
                alignment_x=AlignmentX.RIGHT,
            )

    ######## PUBLIC PROPERTIES ########

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
