from dataclasses import dataclass
from typing import Optional

from neoscore.utils.rect import Rect
from neoscore.utils.units import Unit


@dataclass
class GlyphInfo:
    """A dataclass for glyph info containing all the avialable
    metadata from the SMuFL font.
    The canonical_name field is set at instantiation,
    the others are populated immediately afterwards.
    """

    canonical_name: str
    """the glyph name e.g. 'gClefFlat1Below"""

    codepoint: str
    """SMuFL hex ID number e.g. "\uF55D"""

    description: str
    """short description of glyph, e.g. 'G clef, flat 1 below"""

    boundary_box: Rect
    """coords to glyph boundary box, e.g. x, y, width, height"""

    advance_width: Unit
    """A converted Unit from original float, e.g. Unit[1.234]"""

    anchors: Optional[dict]
    """a variety of additional cut outs, e.g. keys:[x_coord, y_coord]"""

    component_glyphs: Optional[list[str]]
    """list of glyphs that make a complex"""






