from dataclasses import dataclass
from typing import Dict, Optional

from neoscore.core.point import Point
from neoscore.core.rect import Rect
from neoscore.core.units import Unit


@dataclass
class GlyphInfo:
    """SMuFL glyph metadata."""

    canonical_name: str
    """The canonical glyph name, e.g. 'gClefFlat1Below'"""

    codepoint: str
    """The glyph as a unicode string, e.g. ``'\\uF55D'``"""

    description: str
    """Short description of glyph, e.g. 'G clef, flat 1 below'"""

    bounding_rect: Optional[Rect]
    """Glyph bounding rect from SMuFL metadata.

    Note that this is not always very accurate. If accurate measurements are needed,
    it's better to query the font with :obj:`.Font.bounding_rect_of`.
    """

    advance_width: Optional[Unit]
    """The typographic advance distance specified for the glyph."""

    anchors: Optional[Dict[str, Point]]
    """A collection of anchor points provided by SMuFL metadata.

    See `SMuFL's docs on anchors
    <https://w3c.github.io/smufl/latest/specification/glyphswithanchors.html>`_. Note
    that, while SMuFL provides anchors in a vertically inverted coordinate system, they
    are automatically translated to neoscore's coordinates here.
    """
