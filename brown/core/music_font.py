from brown.interface.font_interface import FontInterface
from brown.core import brown
from brown.core.font import Font
from brown.utils import smufl
from brown.utils.point import Point
from brown.utils.rect import Rect
from brown.utils.units import convert_all_to_unit


class MusicFontMetadataNotFoundError(Exception):
    """Exception raised when metadata for a music font can't be found."""
    pass


class MusicFontGlyphNotFoundError(Exception):
    """Exception raised when a glyph cannot be found in a MusicFont"""
    pass


class MusicFont(Font):

    """A SMuFL compliant music font"""

    _interface_class = FontInterface

    def __init__(self, family_name, staff_unit):
        self.unit = staff_unit
        try:
            self.metadata = brown.registered_music_fonts[family_name]
            # Convert all metadata values to staff units
            convert_all_to_unit(self.metadata, self.unit)
        except KeyError:
            raise MusicFontMetadataNotFoundError
        self._engraving_defaults = self.metadata['engravingDefaults']
        # TODO: Investigate why staff_unit(3) is the
        #       magic scaling factor here, and how to not rely on it
        self._em_size = self.unit(3)
        super().__init__(family_name, self._em_size, 1, False)

    ######## PUBLIC PROPERTIES ########

    @property
    def em_size(self):
        """GraphicUnit: The em size for the font."""
        return self._em_size

    @property
    def engraving_defaults(self):
        """dict: The SMuFL engraving defaults information for this font"""
        return self._engraving_defaults

    ######## PUBLIC METHODS ########

    def glyph_info(self, glyph_name, alternate_number=None):
        """Collect and return all known metadata about a glyph.

        Args:
            glyph_name (str): The canonical name of the glyph
            alternate_number (int or None): A glyph alternate number

        Returns:
            None: If the glyph is not available in the font
            dict: A collection of all known metadata about the glyph

        Raises:
            MusicFontGlyphNotFoundError: If the requested glyph
                could not be found in the font.
        """
        info = {}
        if alternate_number:
            try:
                alternate = self.metadata['glyphsWithAlternates'][
                                          glyph_name][
                                          'alternates'][
                                          alternate_number - 1]
                info['codepoint'] = alternate['codepoint']
                real_name = alternate['name']
            except KeyError:
                # Alternate not found in the font
                raise MusicFontGlyphNotFoundError
        else:
            try:
                info['codepoint'] = smufl.glyph_names[glyph_name]['codepoint']
            except KeyError:
                raise MusicFontGlyphNotFoundError
            real_name = glyph_name

        try:
            info['description'] = smufl.glyph_names[real_name]['description']
        except KeyError:
            pass
        try:
            info['classes'] = smufl.get_glyph_classes(real_name)
        except KeyError:
            pass
        try:
            info["glyphBBox"] = self.metadata['glyphBBoxes'][real_name]
        except KeyError:
            pass
        try:
            info['alternates'] = self.metadata[
                'glyphsWithAlternates'][real_name]['alternates']
        except KeyError:
            pass
        try:
            info['anchors'] = self.metadata['glyphsWithAnchors'][real_name]
        except KeyError:
            pass
        try:
            info['componentGlyphs'] = self.metadata['ligatures'][real_name]['componentGlyphs']
        except KeyError:
            pass
        for set_key in self.metadata['sets'].keys():
            for glyph in self.metadata['sets'][set_key]['glyphs']:
                if glyph['alternateFor'] == real_name:
                    info['setAlternatives'] = {}
                    info['setAlternatives'][set_key] = {}
                    info['setAlternatives'][set_key]['description'] = self.metadata['sets'][set_key]['description']
                    info['setAlternatives'][set_key]['name'] = glyph['name']
                    info['setAlternatives'][set_key]['codepoint'] = glyph['codepoint']
        if not info:
            raise MusicFontGlyphNotFoundError
        info['is_optional'] = real_name in self.metadata['optionalGlyphs']
        info['canonicalName'] = real_name
        return info

    def text_bounding_rect(self,
                           music_chars,
                           origin_offset=None,
                           scale_factor=1):
        """Find the bounding rect of a list of MusicChars in this font.

        Args:
            music_chars (list[MusicChar]): The string to represent
            origin_offset (Point): An optional offset to be applied
                to the bounding rect.
            scale_factor (float): The scale factor applied to the text.

        Returns:
            Rect: The bounding rect of the given text if drawn.

        Raises:
            ValueError: if `music_chars` is empty.
        """
        # TODO: This is still a little off...
        if not music_chars:
            raise ValueError('Cannot find the bounding rect of an '
                             'empty character sequence.')
        origin_offset = (origin_offset if origin_offset
                         else Point(self.unit(0), self.unit(0)))
        x = music_chars[0].glyph_info['glyphBBox']['bBoxSW'][0]
        y = music_chars[0].glyph_info['glyphBBox']['bBoxNE'][1]
        w = self.unit(0)
        h = self.unit(0)
        for char in music_chars:
            char_x = char.glyph_info['glyphBBox']['bBoxSW'][0]
            char_y = char.glyph_info['glyphBBox']['bBoxNE'][1]
            w += char.glyph_info['glyphBBox']['bBoxNE'][0] - char_x
            h += (char.glyph_info['glyphBBox']['bBoxSW'][1] - char_y) * -1
        return Rect((x + origin_offset.x) * scale_factor,
                    (y + origin_offset.y) * scale_factor,
                    w * scale_factor,
                    h * scale_factor)
