from brown.core.multi_staff_object import MultiStaffObject
from brown.core.music_font import MusicFontGlyphNotFoundError
from brown.core.music_text_object import MusicTextObject
from brown.utils.units import GraphicUnit


class Brace(MultiStaffObject, MusicTextObject):

    """A brace spanning staves, recurring at line beginnings.

    The brace is drawn at the beginning of every line
    and after its initial x position through its length.
    A brace will be drawn on the first line it appears on
    if and only if it is placed *exactly* at the line beginning.

    Consequently, `Brace(Mm(0), Mm(1000), some_staves)` will appear
    on the first line of the flowable, while
    `Brace(Mm(1), Mm(1000), some_staves) will not begin drawing
    until the second line.
    """

    def __init__(self, pos_x, length, staves):
        """
        Args:
            pos_x (Unit): Where this brace goes into effect
            length (Unit): How long this brace is in effect
            staves (set{Staff}): The staves this brace spans
        """
        MultiStaffObject.__init__(self, staves)
        # Calculate the height of the brace in highest_staff staff units
        scale = self.vertical_span / self.highest_staff.unit(4)
        if self.vertical_span > self.highest_staff.unit(50):
            text = ('brace', 4)
        elif self.vertical_span > self.highest_staff.unit(30):
            text = ('brace', 3)
        elif self.vertical_span > self.highest_staff.unit(15):
            text = ('brace', 2)
        elif self.vertical_span > self.highest_staff.unit(4):
            text = 'brace'
        else:
            text = ('brace', 1)
        try:
            # Attempt to use size-specific optional glyph
            MusicTextObject.__init__(self,
                                     (pos_x, self.vertical_span),
                                     text,
                                     self.highest_staff,
                                     scale_factor=scale)
        except MusicFontGlyphNotFoundError:
            # Default to non-optional glyph
            MusicTextObject.__init__(self,
                                     (pos_x, self.vertical_span),
                                     'brace',
                                     self.highest_staff,
                                     scale_factor=scale)
        self._breakable_width = length

    ######## PUBLIC PROPERTIES ########

    @property
    def breakable_width(self):
        """Unit: The breakable width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self._breakable_width

    ######## PRIVATE METHODS ########

    def _render_before_break(self, local_start_x, start, stop):
        if start.x == GraphicUnit(0):
            self._render_complete(start)

    def _render_after_break(self, local_start_x, start, stop):
        self._render_complete(start)

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_complete(start)
