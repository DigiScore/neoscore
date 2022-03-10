from dataclasses import dataclass, field
from typing import Optional

from brown.core.music_font import MusicFont
from brown.utils.rect import Rect


@dataclass(frozen=True)
class MusicChar:
    """A SMuFL music character."""

    font: MusicFont
    """The font used to derive SMuFL spec information about this glyph."""

    glyph_name: str
    """The canonical SMuFL name of the glyph"""

    alternate_number: Optional[int] = None
    """An SMuFL alternate glyph code, if applicable."""

    glyph_info: dict = field(init=False, hash=False, compare=False, repr=False)
    """SMuFL data on the glyph sized to `self.font`"""

    def __post_init__(self):
        super().__setattr__(
            "glyph_info", self.font.glyph_info(self.glyph_name, self.alternate_number)
        )

    ######## PUBLIC PROPERTIES ########

    @property
    def canonical_name(self):
        """The canonical SMuFL glyph name.

        This is a convenience property for `glyph_info["canonicalName"]`
        """
        return self.glyph_info["canonicalName"]

    @property
    def codepoint(self):
        """The glyph's SMuFL codepoint.

        This is a convenience property for `glyph_info["codepoint"]`
        """
        return self.glyph_info["codepoint"]

    @property
    def bounding_rect(self):
        """Rect: The glyph bounding box."""
        x = self.glyph_info["glyphBBox"]["bBoxSW"][0]
        y = self.glyph_info["glyphBBox"]["bBoxNE"][1]
        w = self.glyph_info["glyphBBox"]["bBoxNE"][0] - x
        h = (self.glyph_info["glyphBBox"]["bBoxSW"][1] - y) * -1
        return Rect(x, y, w, h)
