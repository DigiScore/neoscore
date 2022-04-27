from dataclasses import dataclass
from typing import Optional

from neoscore.core.color import ColorDef
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import Union, Unit

# NOTE: When creating a new style, be sure to add it to ALL_STYLES at
# the end of this file.


@dataclass(frozen=True)
class BarlineStyle:
    """Style for an individual sub-barline.

    Use multiple of these to specify multi-part lines like double barlines.
    Format is right to left.
    """

    thickness: Union[str, float, Unit]
    """Thickness of the barline can be 
    engraving default key / pseudo-staff-units / units"""

    gap_right: Union[str, float, Unit] = 0.4
    """Separation gap between grouped barlines, can be 
     engraving default key / pseudo-staff-units / units"""

    pattern: PenPattern = PenPattern.SOLID
    """Line pattern of a barline"""

    color: Optional[ColorDef] = None
    """Colour of a barline"""


SINGLE = [BarlineStyle("thinBarlineThickness")]

THIN_DOUBLE = [
    BarlineStyle("thinBarlineThickness"),
    BarlineStyle("thinBarlineThickness"),
]

END = [
    BarlineStyle("thickBarlineThickness"),
    BarlineStyle("thinBarlineThickness", "thinThickBarlineSeparation"),
]

ALL_STYLES: list[list[BarlineStyle]] = [SINGLE, THIN_DOUBLE, END]
