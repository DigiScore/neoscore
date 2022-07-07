from __future__ import annotations

from backports.cached_property import cached_property

from neoscore.core.glyph_info import GlyphInfo
from neoscore.core.music_char import MusicChar
from neoscore.core.music_font import MusicFont


class RawMusicChar(MusicChar):
    """A music char defined directly by a unicode character"""

    def __init__(self, font: MusicFont, codepoint: str):
        """
        Args:
            font: The character's font
            codepoint: The character's raw unicode string representation.
        """
        self._codepoint = codepoint  # noqa
        super().__init__(font, "[RAW CHAR]")

    @cached_property
    def glyph_info(self) -> GlyphInfo:
        """SMuFL metadata for this character"""
        return GlyphInfo(self.glyph_name, self._codepoint, "", None, None, None)
