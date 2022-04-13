from dataclasses import dataclass
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.music_font import MusicFont

# NOTE: When creating a new style, be sure to add it to ALL_STYLES at
# the end of this file.

@dataclass #(frozen=True)
class BarLineStyle:
    """Bar line styles

    This dataclass outlines the default engraving for
    a number of bar line styles.

    Using this model it is possible to define costume
    bar line styles.
    """

    pattern: PenPattern
    """The line type such as solid or dashed"""

    lines: list
    """a list containing the number and type of lines that 
    make up a bar line style. Listed left to right."""

    separation: str = "barlineSeparation"
    """the default engraving value for separating double bar
    lines. Default is barlineSeparation."""

SINGLE = BarLineStyle(
    PenPattern.SOLID,
    ["thinBarlineThickness"]
)
"""Single line style. Used for normal bar separation."""

THICK = BarLineStyle(
    PenPattern.SOLID,
    ["thickBarlineThickness"]
)
"""Single thick line style."""

THICK_DOUBLE = BarLineStyle(
    PenPattern.SOLID,
    ["thickBarlineThickness",
     "thickBarlineThickness"]
)
"""Think double bar line. Used for end of score."""

THIN_DOUBLE = BarLineStyle(
    PenPattern.SOLID,
    ["thinBarlineThickness",
     "thinBarlineThickness"]
)
"""This double bar line. Used for section separation."""

END = BarLineStyle(
    PenPattern.SOLID,
    ["thinBarlineThickness",
     "thickBarlineThickness"],
    "thinThickBarlineSeparation"
)
"""End bar line, thin solid, then thick solid"""

DASHED = BarLineStyle(
    PenPattern.DASH,
    ["thinBarlineThickness"]
)
"""Dashed single bar line."""


ALL_STYLES: list[BarLineStyle] = [
    SINGLE,
    THICK,
    THICK_DOUBLE,
    THIN_DOUBLE,
    END,
    DASHED,
]
"""A list of all the bar line tables in this module"""