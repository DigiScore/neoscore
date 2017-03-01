from brown.core.text_object import TextObject
from brown.primitives.staff_object import StaffObject
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import Unit
from brown.core.music_char import MusicChar


class MusicTextObject(TextObject, StaffObject):
    """
    A glyph with a MusicFont and convenient access to relevant SMuFL metadata.

    The text content of a MusicTextObject should be a single character.
    Rather than being specified by their unicode codepoints or literals,
    characters should be specified by their canonical SMuFL names.
    """
    def __init__(self, pos, text, parent, font=None, scale_factor=1):
        """
        Args:
            pos (Point): The position of the glyph
            text (str, tuple, MusicChar, or list of these):
                The text to be used, represented as a str (glyph name), tuple
                (glyph name, alternate number), MusicChar, or a list of them.
            parent (GraphicObject): The parent of the glyph. This should
                either be a `Staff` or an object which has a `Staff` as
                an ancestor.
            font (MusicFont): The music font to be used. If not specified,
                the font is taken from the ancestor staff.
            scale_factor (float): A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        if font is None:
            font = StaffObject._find_staff(parent).music_font
        if isinstance(text, str):
            self.music_chars = [MusicChar(font, text)]
        elif isinstance(text, tuple):
            self.music_chars = [MusicChar(font, *text)]
        elif isinstance(text, MusicChar):
            self.music_chars = [text]
        elif isinstance(text, list):
            self.music_chars = []
            for music_char in text:
                if isinstance(music_char, str):
                    self.music_chars.append(MusicChar(font, music_char))
                elif isinstance(music_char, tuple):
                    self.music_chars.append(MusicChar(font, *music_char))
                elif isinstance(music_char, MusicChar):
                    self.music_chars.append(music_char)
                else:
                    raise TypeError
        else:
            raise TypeError
        text = ''.join(char.codepoint for char in self.music_chars)
        TextObject.__init__(self, pos, text, font, parent,
                            scale_factor=scale_factor)
        StaffObject.__init__(self, parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def breakable_width(self):
        """Unit: The breakable width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self._bounding_rect.width

    ######## PRIVATE PROPERTIES ########

    @property
    def _bounding_rect(self):
        """Rect: The bounding rect for this text when rendered."""
        return self.font.text_bounding_rect(self.music_chars,
                                            self._origin_offset,
                                            self.scale_factor)

    @property
    def _origin_offset(self):
        """Point: The origin offset override for this glyph."""
        return Point(self.staff.unit(0),
                     self.staff.unit(self.font.ascent))
