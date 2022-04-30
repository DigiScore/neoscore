from dataclasses import dataclass
from typing import Optional

from neoscore.core.color import ColorDef
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import Union, Unit


@dataclass(frozen=True)
class BarlineStyle:
    """Style for an individual sub-barline.

    Use multiple of these to specify multi-part lines like double barlines.
    """

    thickness: Union[str, float, Unit] = 0.16
    """Thickness for this line

    This can be defined either as a SMuFL engraving default key, a float value of
    pseudo-staff-units, or a plain unit value.
    """

    gap_right: Union[str, float, Unit] = 0.4
    """The gap to the right of this line, if another follows.

    Like ``thickness``, this can be defined either as a SMuFL engraving default key, a
    float value of pseudo-staff-units, or a plain unit value.
    """

    pattern: PenPattern = PenPattern.SOLID
    """Line pattern of a line"""

    color: Optional[ColorDef] = None
    """Color of a line"""


# NOTE: When adding a new style, be sure to add it to ALL_STYLES below

SINGLE = [BarlineStyle("thinBarlineThickness")]

DASH = [BarlineStyle("thinBarlineThickness", pattern=PenPattern.DASH)]

DOT = [BarlineStyle("thinBarlineThickness", pattern=PenPattern.DOT)]

THIN_DOUBLE = [
    BarlineStyle("thinBarlineThickness", "barlineSeparation"),
    BarlineStyle("thinBarlineThickness"),
]

END = [
    BarlineStyle("thinBarlineThickness", "thickBarlineSeparation"),
    BarlineStyle("thickBarlineThickness"),
]

ALL_STYLES: list[list[BarlineStyle]] = [SINGLE, DASH, DOT, THIN_DOUBLE, END]
