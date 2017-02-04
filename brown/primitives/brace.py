from brown.core.graphic_object import GraphicObject
from brown.core.music_text_object import MusicTextObject
from brown.core.recurring_object import RecurringObject
from brown.primitives.multi_staff_object import MultiStaffObject
from brown.core.music_font import MusicFontGlyphNotFoundError


class Brace(RecurringObject, MultiStaffObject, MusicTextObject):

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
        print(f'using brace {text}')
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
        # Recur at line start
        RecurringObject.__init__(self, 0)

    def _render_occurence(self, pos):
        self._render_complete(pos)
