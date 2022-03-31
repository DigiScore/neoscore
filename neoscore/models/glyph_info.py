from dataclasses import dataclass, field
from typing import Optional

from neoscore.utils.units import Unit


@dataclass
class GlyphInfo:
    """A dataclass for glyph info containing all the avialable
    metadata from the SMuFL font.
    The canonical_name field is set at instantiation,
    the others are populated immediately afterwards.

    Args:
        ## ALL GLYPHS WILL RETURN THESE
        canonical_name: str, set at instantiation e.g. 'gClefFlat1Below'
        codepoint: hex number e.g. "\uF55D"
        description: str, e.g. 'G clef, flat 1 below'
        glyphAdvanceWidths: float, e.g. 1.234.
        glyphBBoxes: BBoxCoords dataclass

        ## OPTIONAL TO CERTAIN TYPES OF GLYPH


    """
    canonical_name: str
    codepoint: hex = field(default="")
    description: str = field(default="")
    glyphAdvanceWidths: float = field(default=0.0)
    glyphBBoxes: BBoxCoords
    glyphsWithAnchors: Optional[dict] = None
    componentGlyphs: Optional[list[str]] = None


@dataclass
class BBoxCoords:
    ne_X: Unit
    ne_Y: Unit
    sw_X: Unit
    sw_Y: Unit
