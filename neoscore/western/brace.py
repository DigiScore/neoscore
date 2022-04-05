from typing import Optional, cast

from neoscore.core.brush import BrushDef
from neoscore.core.music_font import MusicFont, MusicFontGlyphNotFoundError
from neoscore.core.music_text import MusicText
from neoscore.core.pen import PenDef
from neoscore.core.point import Point
from neoscore.core.units import ZERO, Unit
from neoscore.western.multi_staff_object import MultiStaffObject, StaffLike


class Brace(MultiStaffObject, MusicText):

    """A brace spanning staves, recurring at line beginnings.

    The brace is drawn at the beginning of every line
    after its initial x position until the end of the staff.

    A brace will be drawn on the first line it appears on
    if and only if it is placed *exactly* at the line beginning.

    Consequently, `Brace(Mm(0), Mm(1000), some_staves)` will appear
    on the first line of the flowable, while
    `Brace(Mm(1), Mm(1000), some_staves)` will not begin drawing
    until the second line.
    """

    def __init__(
        self,
        pos_x: Unit,
        staves: list[StaffLike],
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
            )

    ######## PUBLIC PROPERTIES ########

    @property
    def breakable_length(self) -> Unit:
        """The breakable width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self.parent.breakable_length - self.x

    ######## PRIVATE METHODS ########

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        if start.x == ZERO:
            self._render_complete(Point(start.x - self.bounding_rect.width, start.y))

    def _render_after_break(self, local_start_x, start):
        self._render_complete(Point(start.x - self.bounding_rect.width, start.y))

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_complete(Point(start.x - self.bounding_rect.width, start.y))
