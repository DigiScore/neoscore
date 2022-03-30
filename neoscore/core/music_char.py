from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from neoscore.core.music_font import MusicFont
from neoscore.utils.rect import Rect
from neoscore.models.glyph_info import GlyphInfo


@dataclass(frozen=True)
class MusicChar:
    """A SMuFL music character.

    Note that measurements in the contained metadata may have slight
    errors and should be used with caution when high precision is
    needed.
    """

    font: MusicFont
    """The font used to derive SMuFL spec information about this glyph."""

    glyph_name: str
    """The canonical SMuFL name of the glyph"""

    alternate_number: Optional[int] = None
    """An SMuFL alternate glyph code, if applicable."""

    ######## PUBLIC PROPERTIES ########

    @cached_property
    def glyph_info(self) -> GlyphInfo:
        # this is a little expensive, so only do it on demand and then cache it
        """The metadata for a specified glyphname"""

        return self.font.glyph_info(self.glyph_name, self.alternate_number)

    @property
    def canonical_name(self):
        """The canonical SMuFL glyph name.

        This is a convenience property for `glyph_info.canonical_name`
        """
        return self.glyph_info.canonical_name

    @property
    def codepoint(self):
        """The glyph's SMuFL codepoint.

        This is a convenience property for glyph_info.codepoint`
        """
        return self.glyph_info.codepoint

    @property
    def bounding_rect(self):
        """Rect: The glyph bounding box."""
        # I think y and h here are wrong...
        x = self.glyph_info.glyphBBox["bBoxSW"][0]
        y = self.glyph_info.glyphBBox["bBoxNE"][1]
        w = self.glyph_info.glyphBBox["bBoxNE"][0] - x
        h = (self.glyph_info.glyphBBox["bBoxSW"][1] - y) * -1
        return Rect(x, y, w, h)


    #
    #
    # @cached_property
    # def glyph_info(self) -> dict:
    #     # this is a little expensive, so only do it on demand and then cache it
    #     return self.font.glyph_info(self.glyph_name, self.alternate_number)
    #
    # @property
    # def canonical_name(self):
    #     """The canonical SMuFL glyph name.
    #
    #     This is a convenience property for `glyph_info["canonicalName"]`
    #     """
    #     return self.glyph_info["canonicalName"]
    #
    # @property
    # def codepoint(self):
    #     """The glyph's SMuFL codepoint.
    #
    #     This is a convenience property for `glyph_info["codepoint"]`
    #     """
    #     return self.glyph_info["codepoint"]
    #
    # @property
    # def bounding_rect(self):
    #     """Rect: The glyph bounding box."""
    #     # I think y and h here are wrong...
    #     x = self.glyph_info["glyphBBox"]["bBoxSW"][0]
    #     y = self.glyph_info["glyphBBox"]["bBoxNE"][1]
    #     w = self.glyph_info["glyphBBox"]["bBoxNE"][0] - x
    #     h = (self.glyph_info["glyphBBox"]["bBoxSW"][1] - y) * -1
    #     return Rect(x, y, w, h)
