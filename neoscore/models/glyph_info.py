from dataclasses import dataclass
from typing import Optional

from neoscore.utils.rect import Rect


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
        glyphsWithAnchors: A variety of keys:[x_coord, y_coord]
        componentGlyphs: list of strings (glyph names)

    """
    canonical_name: str
    codepoint: str
    description: str
    boundary_box: Rect
    advance_width: float
    anchors: Optional[dict]
    component_glyphs: Optional[list[str]]






