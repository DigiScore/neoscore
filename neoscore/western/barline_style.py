from dataclasses import dataclass
from typing import List, Optional

from neoscore.core.color import ColorDef
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import Union, Unit


@dataclass(frozen=True)
class BarlineStyle:
    """Style for an individual sub-barline.

    Use multiple of these to specify multipart lines like double barlines.
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
    """Line pattern of this line"""

    color: Optional[ColorDef] = None
    """Color of this line given as a :obj:`.ColorDef`"""


# NOTE: When adding a new style, be sure to add it to ALL_STYLES below

SINGLE = [BarlineStyle("thinBarlineThickness")]
"""A plain single barline."""

DASH = [BarlineStyle("thinBarlineThickness", pattern=PenPattern.DASH)]
"""A single dashed barline."""

DOT = [BarlineStyle("thinBarlineThickness", pattern=PenPattern.DOT)]
"""A single dotted barline."""

THIN_DOUBLE = [
    BarlineStyle("thinBarlineThickness", "barlineSeparation"),
    BarlineStyle("thinBarlineThickness"),
]
"""A thin double barline."""

END = [
    BarlineStyle("thinBarlineThickness", "thickBarlineSeparation"),
    BarlineStyle("thickBarlineThickness"),
]
"""A thick double barline conventionally used at the end of scores."""

ALL_STYLES: List[List[BarlineStyle]] = [SINGLE, DASH, DOT, THIN_DOUBLE, END]
