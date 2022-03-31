from dataclasses import dataclass, field
from typing import Optional

from neoscore.utils.units import Unit


@dataclass
class BBoxCoords:
    """A dataclass that holds the boundary box coords
    for a SMuFL glyph.

    Args:
        bBoxNE_X: Unit, x coord for north-east of box
        bBoxNE_Y: Unit, y coord for north-east of box
        bBoxSW_X: Unit, x coord for south-west of box
        bBoxSW_Y: Unit, y coord for south-west of box
    """

    bBoxNE_X: Unit
    bBoxNE_Y: Unit
    bBoxSW_X: Unit
    bBoxSW_Y: Unit

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
    codepoint: hex = field(default="")
    description: str = field(default="")
    glyphBBoxes: BBoxCoords = field(default=None)
    glyphAdvanceWidths: float = field(default=0.0)
    glyphsWithAnchors: Optional[dict] = None
    componentGlyphs: Optional[list[str]] = None






