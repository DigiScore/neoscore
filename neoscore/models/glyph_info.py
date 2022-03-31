from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GlyphInfo:
    """A dataclass for glyph info containing all the avialable
    metadata from the SMuFL font.
    The canonical_name field is set at instantiation,
    the others are populated immediately afterwards.

    Args:
        canonical_name: str, set at instantiation e.g. 'gClefFlat1Below'
        codepoint: hex number e.g. "\uF55D"
        description: str, e.g. 'G clef, flat 1 below'
        glyphAdvanceWidths: float, e.g.

    """
    canonical_name: str
    codepoint: hex = field(default="")
    description: str = field(default="")
    glyphAdvanceWidths: Optional[float] = field(default=0.0)
    glyphBBoxes: Optional[dict] = None
    glyphsWithAnchors: Optional[dict] = None
    componentGlyphs: Optional[list] = None
