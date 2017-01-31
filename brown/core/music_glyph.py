from brown.core.text_object import TextObject
from brown.core.music_font import MusicFont
from brown.primitives.staff_object import StaffObject
from brown.utils.rect import Rect
from brown.utils.point import Point


class MusicGlyph(TextObject, StaffObject):
    """
    A glyph with a MusicFont and convenient access to relevant SMuFL metadata.

    The text content of a MusicGlyph should be a single character.
    Rather than being specified by their unicode codepoints or literals,
    characters should be specified by their canonical SMuFL names.
    """

    def __init__(self, pos, canonical_name, font=None,
                 parent=None, scale_factor=1):
        """
        Args:
            pos (Point): The position of the glyph
            canonical_name (str): The canonical SMuFL name of the glyph
            font (MusicFont): The music font to be used. If not specified,
                the font is taken from the ancestor staff.
            parent (GraphicObject): The parent of the glyph. This should
                either be a `Staff` or an object which has a `Staff` as
                an ancestor.
                    TODO: parent field should be mandatory!
            scale_factor (float): A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        if font is None:
            staff = StaffObject._find_staff(parent)
            font = staff.music_font
        elif not isinstance(font, MusicFont):
            raise TypeError('MusicGlyph.font must be of type MusicFont')
        # type check font is MusicFont before sending to init?
        self._canonical_name = canonical_name
        codepoint = font.glyph_info(self.canonical_name)['codepoint']
        TextObject.__init__(self, pos, codepoint, font, parent,
                            scale_factor=scale_factor)
        StaffObject.__init__(self, parent)
        self._generate_glyph_info()

    ######## PUBLIC PROPERTIES ########

    @property
    def canonical_name(self):
        """str: The canonical name of the glyph"""
        return self._canonical_name

    @property
    def glyph_info(self):
        """dict: The aggregated SMuFL metadata for this glyph"""
        try:
            return self._glyph_info
        except AttributeError:
            self._generate_glyph_info()
            return self._glyph_info

    @property
    def font(self):
        """MusicFont: The glyph music font."""
        return self._font

    @font.setter
    def font(self, value):
        # TODO: Code below is redundant with super,
        #       find a way to use inheritance here
        if not isinstance(value, MusicFont):
            raise TypeError('MusicGlyph.font must be a MusicFont')
        self._font = value

    ######## PRIVATE PROPERTIES ########

    @property
    def _bounding_rect(self):
        """Rect: The bounding rect for this glyph."""
        # TODO: This is still a little off...
        x = self.glyph_info['glyphBBox']['bBoxSW'][0]
        y = self.glyph_info['glyphBBox']['bBoxNE'][1]
        w = self.glyph_info['glyphBBox']['bBoxNE'][0] - x
        h = (self.glyph_info['glyphBBox']['bBoxSW'][1] - y) * -1
        return Rect(x, y, w, h)

    @property
    def _origin_offset(self):
        """Point: The origin offset override for this glyph."""
        return Point(self.staff.unit(0),
                     self.staff.unit(self.font.ascent))

    ######## PRIVATE METHODS ########

    def _generate_glyph_info(self):
        """Find and generate SMuFL metadata for the glyph.

        This converts all numeric measurements to real StaffUnit values.

        Returns:
            dict: The aggregated SMuFL metadata for this glyph
        """
        self._glyph_info = self.font.glyph_info(self.canonical_name)
