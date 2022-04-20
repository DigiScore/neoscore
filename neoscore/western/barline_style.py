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


SINGLE = (BarlineStyle("thinBarlineThickness"),)

THIN_DOUBLE = (
    BarlineStyle("thinBarlineThickness"),
    BarlineStyle("thinBarlineThickness"),
)

END = (
    BarlineStyle("thinBarlineThickness", "thinThickBarlineSeparation"),
    BarlineStyle("thickBarlineThickness"),
)

ALL_STYLES: list[tuple[BarlineStyle]] = [SINGLE, THIN_DOUBLE, END]


# @dataclass(frozen=True)
# class BarlineStyle:
#     """Barline styles
#
#     This dataclass outlines the default engraving for
#     a number of barline styles.
#
#     Using this model it is possible to define costume
#     barline styles.
#     """
#
#     pattern: PenPattern
#     """The line type such as solid or dashed"""
#
#     lines: list
#     """a list containing the number and type of lines that
#     make up a bar line style. Listed left to right."""
#
#     separation: str = "barlineSeparation"
#     """the default engraving value for separating double bar
#     lines. Default is barlineSeparation."""
#
#
# SINGLE = BarlineStyle(PenPattern.SOLID, ["thinBarlineThickness"])
# """Single line style. Used for normal bar separation."""
#
# THICK = BarlineStyle(PenPattern.SOLID, ["thickBarlineThickness"])
# """Single thick line style."""
#
# THICK_DOUBLE = BarlineStyle(
#     PenPattern.SOLID, ["thickBarlineThickness", "thickBarlineThickness"]
# )
# """Think double bar line. Used for end of score."""
#
# THIN_DOUBLE = BarlineStyle(
#     PenPattern.SOLID, ["thinBarlineThickness", "thinBarlineThickness"]
# )
# """This double bar line. Used for section separation."""
#
# END = BarlineStyle(
#     PenPattern.SOLID,
#     ["thinBarlineThickness", "thickBarlineThickness"],
#     "thinThickBarlineSeparation",
# )
# """End bar line, thin solid, then thick solid"""
#
# DASHED = BarlineStyle(PenPattern.DASH, ["thinBarlineThickness"])
# """Dashed single bar line."""
#
#
# ALL_STYLES: list[BarlineStyle] = [
#     SINGLE,
#     THICK,
#     THICK_DOUBLE,
#     THIN_DOUBLE,
#     END,
#     DASHED,
# ]
# """A list of all the bar line tables in this module"""
