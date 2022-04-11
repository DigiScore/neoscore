from enum import Enum
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.music_font import MusicFont

class BarLineStyle(Enum):
    """Bar line styles

    Bar line

    textFontFamily
    repeatBarlineDotSeparation
    thinThickBarlineSeparation
    barlineSeparation
    thickBarlineThickness
    thinBarlineThickness

      """
    # engraving_defaults = MusicFont.engraving_defaults


    SINGLE = {"pattern": PenPattern.SOLID,
              "lines": ["thinBarlineThickness"],
              "separation": None}
    """Single line style. Used for normal bar separation."""

    THICK_DOUBLE = {"pattern": PenPattern.SOLID,
                    "lines": ["thickBarlineThickness",
                              "thickBarlineThickness"],
                    "separation": "barlineSeparation"}
    """Think double bar line. Used for end of score."""

    THIN_DOUBLE = {"pattern": PenPattern.SOLID,
                   "lines": ["thinBarlineThickness",
                        "thinBarlineThickness"],
                   "separation": "barlineSeparation"}
    """This double bar line. Used for section separation."""

    END = {"pattern": PenPattern.SOLID,
              "lines": ["thinBarlineThickness",
                        "thinBarlineThickness"],
           "separation": "thinThickBarlineSeparation"}
    """End bar line, thin solid, then thick solid"""

    DASHED = {"pattern": PenPattern.DASH,
              "lines": ["thinBarlineThickness"],
              "separation": None}
    """Dashed single bar line."""
