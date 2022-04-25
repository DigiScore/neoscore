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
    """

    thickness: Union[str, float, Unit]
    gap_right: Union[str, float, Unit] = 0.4
    pattern: PenPattern = PenPattern.SOLID
    color: Optional[ColorDef] = None


SINGLE = [BarlineStyle("thinBarlineThickness")]

THIN_DOUBLE = [
    BarlineStyle("thinBarlineThickness"),
    BarlineStyle("thinBarlineThickness"),
]

END = [
    BarlineStyle("thinBarlineThickness", "thinThickBarlineSeparation"),
    BarlineStyle("thickBarlineThickness"),
]

ALL_STYLES: list[list[BarlineStyle]] = [SINGLE, THIN_DOUBLE, END]
