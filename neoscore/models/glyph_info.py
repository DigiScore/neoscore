from dataclasses import dataclass
from typing import Optional

from neoscore.utils.rect import Rect
from neoscore.utils.units import Unit


@dataclass
class GlyphInfo:
    """A dataclass for glyph info containing the essential
    metadata from the SMuFL font for use in Neoscore
    """

    canonical_name: str
    """the glyph name e.g. 'gClefFlat1Below"""

    codepoint: str
    """the glyph as a unicode string e.g. "\uF55D"""

    description: str
    """short description of glyph, e.g. 'G clef, flat 1 below"""

    bounding_box: Optional[Rect]
    """Glyph bounding rect from SMuFL metadata"""

    advance_width: Optional[Unit]
    """Determines the degree of overlap of a glyph, e.g. Unit[1.234]"""

    anchors: Optional[dict]
    """a variety of additional metadata from SMuFL 
    such as cutOut, splitStems, stemDirection, graceNote"""







