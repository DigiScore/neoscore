from neoscore.core.mapping import map_between_x
from neoscore.core.music_font import MusicFontGlyphNotFoundError
from neoscore.core.music_text import MusicText
from neoscore.utils.point import Point
from neoscore.utils.units import ZERO, Unit
from neoscore.western.multi_staff_object import MultiStaffObject
from neoscore.western.staff import Staff
from neoscore.western.staff_object import StaffObject


class Brace(MultiStaffObject, StaffObject, MusicText):

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

    def __init__(self, pos_x: Unit, staves: set[Staff]):
        """
        Args:
            pos_x (Unit): Where this brace goes into effect
            staves (set(Staff)): The staves this brace spans
        """
        MultiStaffObject.__init__(self, staves)
        StaffObject.__init__(self, self.highest_staff)
        # Calculate the height of the brace in highest_staff staff units
        scale = self.vertical_span / self.highest_staff.unit(4)
        if self.vertical_span > self.highest_staff.unit(50):
            text = ("brace", 4)
        elif self.vertical_span > self.highest_staff.unit(30):
            text = ("brace", 3)
        elif self.vertical_span > self.highest_staff.unit(15):
            text = ("brace", 2)
        elif self.vertical_span > self.highest_staff.unit(4):
            text = "brace"
        else:
            text = ("brace", 1)
        try:
            # Attempt to use size-specific optional glyph
            MusicText.__init__(
                self, (pos_x, self.vertical_span), self.highest_staff, text, scale=scale
            )
        except MusicFontGlyphNotFoundError:
            # Default to non-optional glyph
            MusicText.__init__(
                self,
                (pos_x, self.vertical_span),
                self.highest_staff,
                "brace",
                scale=scale,
            )

    ######## PUBLIC PROPERTIES ########

    @property
    def breakable_length(self):
        """Unit: The breakable width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self.staff.breakable_length - map_between_x(self.staff, self)

    ######## PRIVATE METHODS ########

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        if start.x == ZERO:
            self._render_complete(Point(start.x - self.bounding_rect.width, start.y))

    def _render_after_break(self, local_start_x, start):
        self._render_complete(Point(start.x - self.bounding_rect.width, start.y))

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_complete(Point(start.x - self.bounding_rect.width, start.y))
