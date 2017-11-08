from brown.core.music_char import MusicChar
from brown.core.staff_object import StaffObject
from brown.core.text import Text
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import GraphicUnit


class MusicText(Text):
    """
    A glyph with a MusicFont and convenient access to relevant SMuFL metadata.
    """
    def __init__(self, pos, text, parent, font=None, scale_factor=1):
        """
        Args:
            pos (Point or init tuple): The position of the text.
            text (str, tuple, MusicChar, or list of these):
                The text to be used, represented as a either a `str`
                (glyph name), `tuple` (glyph name, alternate number),
                `MusicChar`, or a list of these.
            parent (GraphicObject): The parent of the glyph. If no `font`
                is given, this must either be a `Staff` or an object which has
                a `Staff` as an ancestor.
            font (MusicFont): The music font to be used. If not specified,
                `parent` must be or have a `Staff` ancestor.
            scale_factor (float): A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        if font is None:
            ancestor_staff = StaffObject.find_staff(parent)
            if ancestor_staff is None:
                raise ValueError('MusicText must be given either a '
                                 'MusicFont or an ancestor staff')
            font = ancestor_staff.music_font
        self.music_chars = MusicText._resolve_music_chars(text, font)
        text = ''.join(char.codepoint for char in self.music_chars)
        Text.__init__(self, pos, text, font, parent,
                      scale_factor=scale_factor)

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self):
        """Unit: The breakable width of the object.

        This is used to determine how and where rendering cuts should be made.
        """
        return self.bounding_rect.width

    ######## PRIVATE PROPERTIES ########

    @property
    def bounding_rect(self):
        """Rect: The bounding rect for this text when rendered."""
        return self._char_list_bounding_rect(self.music_chars)

    @property
    def _origin_offset(self):
        """Point: The origin offset override for this glyph."""
        return Point(GraphicUnit(0),
                     self.font.ascent)

    ######## PRIVATE METHODS ########

    def _char_list_bounding_rect(self, music_chars):
        """Find the bounding rect of a given list of music chars.

        Takes a list of MusicChars and determined the bounding rect
        they would have if they were in this MusicText.

        The fonts of every music character should the the same as self.font.

        Args:
            music_chars (list[MusicChar]): The string to represent

        Returns:
            Rect: The bounding rect of the specified text if drawn.

        Raises:
            ValueError: if `music_chars` is empty.
        """
        if not music_chars:
            raise ValueError('Cannot find the bounding rect of an '
                             'empty character sequence.')
        x = music_chars[0].glyph_info['glyphBBox']['bBoxSW'][0]
        y = music_chars[0].glyph_info['glyphBBox']['bBoxNE'][1]
        w = GraphicUnit(0)
        h = GraphicUnit(0)
        for char in music_chars:
            char_x = char.glyph_info['glyphBBox']['bBoxSW'][0]
            char_y = char.glyph_info['glyphBBox']['bBoxNE'][1]
            w += char.glyph_info['glyphBBox']['bBoxNE'][0] - char_x
            h += (char.glyph_info['glyphBBox']['bBoxSW'][1] - char_y) * -1
        return Rect((x + self._origin_offset.x) * self.scale_factor,
                    (y + self._origin_offset.y) * self.scale_factor,
                    w * self.scale_factor,
                    h * self.scale_factor)

    @staticmethod
    def _resolve_music_chars(text, font):
        """
        Args:
            text (str, tuple, MusicChar, or list of these):
                The text to be used, represented as a either a `str`
                (glyph name), `tuple` (glyph name, alternate number),
                `MusicChar`, or a list of these.
            font (MusicFont): The font to be applied to the text
        """
        if isinstance(text, str):
            return [MusicChar(font, text)]
        elif isinstance(text, tuple):
            return [MusicChar(font, *text)]
        elif isinstance(text, MusicChar):
            return [text]
        elif isinstance(text, list):
            music_chars = []
            for music_char in text:
                if isinstance(music_char, str):
                    music_chars.append(MusicChar(font, music_char))
                elif isinstance(music_char, tuple):
                    music_chars.append(MusicChar(font, *music_char))
                elif isinstance(music_char, MusicChar):
                    music_chars.append(music_char)
                else:
                    raise TypeError
            return music_chars
        else:
            raise TypeError
